# Basic Imports
from typing import Annotated, Union
from typing_extensions import TypedDict
from pathlib import Path
import dotenv

# LangGraph Imports
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

# Local Imports
from prompts import authenticator_prompt_content, information_prompt_content
from nodes import (
    StartNode,
    AuthenticatorAgentNode,
    AuthenticatorToolNode,
    InformationAgentNode,
    AuthenticatorOrInfoRouter,
    ToolRouter,
)

# Constants
DATABASES_PATH = Path(__file__).parent.parent.joinpath("data").joinpath("databases")

# Loading env-variables
_ = dotenv.load_dotenv(dotenv.find_dotenv())

def build_graph(model=None):
    # Variables
    memory = SqliteSaver.from_conn_string(DATABASES_PATH.joinpath("memory.db"))

    # Graph State
    class State(TypedDict):
        messages: Annotated[list, add_messages]
        is_authenticated: Union[bool, None]
        cpf: Union[str, None]
        data_nascimento: Union[str, None]
        nome: Union[str, None]
        opcoes_pagamento: Union[str, None]
        valor_atual_divida: Union[str, None]
        data_origem_divida: Union[str, None]
        loja: Union[str, None]
        produto: Union[str, None]


    # Graph Design and State
    graph_builder = StateGraph(State)

    # Graph Nodes
    graph_builder.add_node("starting_node", StartNode())
    graph_builder.add_node(
        "authenticator_agent",
        AuthenticatorAgentNode(model=model, prompt=authenticator_prompt_content),
    )
    graph_builder.add_node("authenticator_tool", AuthenticatorToolNode())
    graph_builder.add_node(
        "information_agent",
        InformationAgentNode(model=model, prompt=information_prompt_content),
    )

    # Graph Routes
    graph_builder.set_entry_point("starting_node")
    graph_builder.add_conditional_edges(
        "starting_node",
        AuthenticatorOrInfoRouter(),
        {
            "to_auth": "authenticator_agent",
            "to_info": "information_agent",
        },
    )
    graph_builder.add_conditional_edges(
        "authenticator_agent",
        ToolRouter(),
        {
            "to_tool": "authenticator_tool",
            "to_user": END,
        },
    )
    graph_builder.add_conditional_edges(
        "authenticator_tool",
        AuthenticatorOrInfoRouter(),
        {
            "to_auth": "authenticator_agent",
            "to_info": "information_agent",
        },
    )
    graph_builder.set_finish_point("information_agent")

    # Compiling graph
    graph = graph_builder.compile(checkpointer=memory)
    
    return graph
