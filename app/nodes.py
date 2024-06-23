# Basic Imports
from datetime import datetime

# LangChain Imports
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate

# Local Imports
from tools import authenticate_user_tool, tools_by_name

# Constants
TODAY = str(datetime.now().date())

# Classes (Nodes)
class StartNode():
    """Starting node. Only required for routing to the correct agent"""
    def __init__(self):
        pass
    def __call__(self, state):
        if not state["is_authenticated"]:
            return {"is_authenticated": False}
        else:
            return state
    

class AuthenticatorAgentNode():
    """Agent responsible for authenticating the user"""
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt

    def __call__(self, state):
        
        authenticator_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompt.format(today=TODAY)),
                ("placeholder", "{messages}"),
            ]
        )
        return {"messages": [(authenticator_prompt | self.model.bind_tools([authenticate_user_tool])).invoke(state)]}
    
    
class AuthenticatorToolNode():
    """Tool execution node for AuthenticatorAgentNode"""
    def __init__(self):
        pass

    def __call__(self, state):
        tool_call = state["messages"][-1].tool_calls[0]
        tool = tools_by_name[tool_call["name"]]
        args = tool_call["args"]
        id = tool_call["id"]
        observation = tool.invoke(args)
        if isinstance(observation, str):
            state["is_authenticated"] = False
            return {"messages": [ToolMessage(content=observation, tool_call_id=id)]}
        else:
            df = observation
            state["is_authenticated"] = True
            state["cpf"] = df["cpf_cnpj"].item()
            state["data_nascimento"] = df["data_nascimento"].item()
            state["nome"] = df["nome"].item()
            state["opcoes_pagamento"] = df["Opcoes_Pagamento"].str.replace('"',"").str.replace("{","{{").str.replace("}","}}").item()
            state["data_origem_divida"] = df["data_origem"].item()
            state["loja"] = df["loja"].item()
            state["produto"] = df["produto"].item()
            state["messages"] = [ToolMessage(content="Usuário autenticado", tool_call_id=id)]
            return state
        

class AuthenticatorOrInfoRouter():
    """Decision node. Routes to the correct agent according to the state of the graph"""
    def __init__(self):
        pass
    def __call__(self, state):
        if state["is_authenticated"]:
            return "to_info"
        else:
            return "to_auth"
            

class ToolRouter():
    """Tool router for any agent that needs to execute tools"""
    def __init__(self):
        pass
    def __call__(self, state):
        print(state)
        if state["messages"][-1].tool_calls:
            return "to_tool"
        else:
            return "to_user"
        

class InformationAgentNode():
    """Agent responsible for providing information to the user"""
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt

    def __call__(self, state):
        information_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt.format(
                payment_options=state["opcoes_pagamento"], 
                product=state["produto"],
                debt_origin_date=state["data_origem_divida"],
                name=state["nome"], 
                store=state["loja"],
                today=TODAY,
            )),
            ("placeholder", "{messages}"),
        ])
        return {"messages": [(information_prompt | self.model).invoke(state)]}