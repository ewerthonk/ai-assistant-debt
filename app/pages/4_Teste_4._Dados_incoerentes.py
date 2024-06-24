# Basic Imports
from pathlib import Path

# Frontend Imports
import streamlit as st

# Local Imports
from utils import load_metadata_from_state_memory, extract_message_for_streamlit

# Constants
RESOURCES_DIR = Path(__file__).parent.parent.parent.joinpath("resources")

# Variables
thread_id = "teste_4"

# Setting page style
st.set_page_config(
    page_title="Teste | Case Acerto",
    page_icon=str(RESOURCES_DIR.joinpath("logo_1.png")),
    layout="wide",
)
st.title("Teste 4. Dados incoerentes")
st.caption(
    "**Caso de teste:** Usuário insere dados que não fazem sentido para um CPF e data de nascimento. \n\n"
    "**Objetivo:** checar se o chatbot pode detectar casos de incoerência."
)
with st.sidebar:
    "[Planejamento](https://docs.google.com/document/d/1KjYd8HR94FH1ZMoEWxI6SCZ_lVyIvGIF_7jPZDHtk9c/edit?usp=sharing)"
    "[Apresentação](https://docs.google.com/presentation/d/1SwAivlGW-JY7K1KCBE56eMsO9HwCef_oI5Y4f8OcEds/edit?usp=sharing)"
    "[Repositório](https://github.com/ewerthonk/ai-assistant-debt)"

# Display chat messages from memory database
## First Message
with st.chat_message(name="assistant", avatar=str(RESOURCES_DIR.joinpath("logo_2.png"))):
    st.markdown(
            "Olá, sou o Chatbot da Acerto. Para que eu possa te ajudar com informações sobre suas dívidas, por favor, "
            "pode me dizer qual é seu CPF e data de nascimento? \n\n"
    )

## All other messages
messages = (
    load_metadata_from_state_memory(thread_id)["metadata"]
    .apply(lambda x: extract_message_for_streamlit(x))
)
for message in messages:
    if message:
        if message["role"] == "user":
            with st.chat_message(name="user"):
                st.markdown(message["content"])
        else:
            with st.chat_message(name=message["role"], avatar=str(RESOURCES_DIR.joinpath("logo_2.png"))):
                st.markdown(message["content"])
