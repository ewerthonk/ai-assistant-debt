# Basic Imports
import os
from pathlib import Path

# Streamlit Imports
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st

# LangChain Imports
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from openai import AuthenticationError, OpenAI

# Local Imports
from graph import build_graph

# Constants
RESOURCES_DIR = Path(__file__).parent.parent.joinpath("resources")

# Chat function
def stream_chat(graph, thread_id, user_input):
    config = {"configurable": {"thread_id": thread_id}}
    for event in graph.stream(
        {"messages": [("user", user_input)]},
        config,
    ):
        if (
            "messages" in list(event.values())[0]
            and isinstance(list(event.values())[0]["messages"][-1], AIMessage)
            and list(event.values())[0]["messages"][-1].content
        ):
            yield ((list(event.values())[0]["messages"][-1].content) + "\n")


# Setting page style
st.set_page_config(
    page_title="Chatbot",
    layout="wide",
)
st.title("Chatbot")
with st.sidebar:
    "[Planejamento](https://docs.google.com/document/d/1KjYd8HR94FH1ZMoEWxI6SCZ_lVyIvGIF_7jPZDHtk9c/edit?usp=sharing)"
    "[Apresentação](https://docs.google.com/presentation/d/1SwAivlGW-JY7K1KCBE56eMsO9HwCef_oI5Y4f8OcEds/edit?usp=sharing)"
    "[Repositório](https://github.com/ewerthonk/ai-assistant-debt)"
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# Initialize the session state
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = get_script_run_ctx().session_id

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": (
                "Olá, sou o Chatbot de débitos. Para que eu possa te ajudar com informações sobre suas dívidas, por favor, "
                "pode me dizer qual é seu CPF e data de nascimento? \n\n"
            ),
        }
    )

if "graph" not in st.session_state:
    st.session_state["graph"] = None

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    if message["role"] == "user":
        with st.chat_message(name="user"):
            st.markdown(message["content"])
    else:
        with st.chat_message(name=message["role"]):
            st.markdown(message["content"])

if not st.session_state["graph"]:
    if not openai_api_key:
        st.info("Adicione sua OpenAI API key para iniciar.")
        st.stop()

    try:
        OpenAI(api_key=openai_api_key).models.list()
        graph = build_graph(
            model=ChatOpenAI(
                    model="gpt-4o",
                    api_key=openai_api_key,
                    temperature=0,
                    max_retries=2,
                )
            )
        st.session_state["graph"] = graph
    except AuthenticationError:
        st.info("A OpenAI API key inserida é inválida.")
        st.stop()

# User Input
if user_message := st.chat_input("Como posso ajudar?"):
    # Display user message in chat message container
    with st.chat_message(name="user"):
        st.markdown(user_message)

    # Display assistant response in chat message container
    with st.chat_message(name="assistant",):
        chatbot_message = st.write_stream(
            stream_chat(
                graph=st.session_state["graph"],
                thread_id=st.session_state["thread_id"],
                user_input=user_message,
            )
        )

    # Add messages to chat history
    st.session_state["messages"].append({"role": "user", "content": user_message})
    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": chatbot_message,
        }
    )
