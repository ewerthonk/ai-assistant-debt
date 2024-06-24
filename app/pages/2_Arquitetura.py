# Basic Imports
from pathlib import Path

# Frontend Imports
import streamlit as st

# Constants
RESOURCES_DIR = Path(__file__).parent.parent.parent.joinpath("resources")

# Setting page style
st.set_page_config(
    page_title="Teste | Case Acerto",
    page_icon=str(RESOURCES_DIR.joinpath("logo_1.png")),
)
st.title("Arquitetura")
with st.sidebar:
    "[Planejamento](https://docs.google.com/document/d/1KjYd8HR94FH1ZMoEWxI6SCZ_lVyIvGIF_7jPZDHtk9c/edit?usp=sharing)"
    "[Apresentação](https://docs.google.com/presentation/d/1SwAivlGW-JY7K1KCBE56eMsO9HwCef_oI5Y4f8OcEds/edit?usp=sharing)"
    "[Repositório](https://github.com/ewerthonk/ai-assistant-debt)"

# Page content
st.image(str(RESOURCES_DIR.joinpath("diagram.png")))