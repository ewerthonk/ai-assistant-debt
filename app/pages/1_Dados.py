# Basic Imports
import dotenv
from pathlib import Path

# Frontend Imports
import streamlit as st

# Local Imports
from ingest import df

_ = dotenv.load_dotenv(dotenv.find_dotenv())

# Constants
RESOURCES_DIR = Path(__file__).parent.parent.joinpath("resources")

st.set_page_config(
    page_title="Dados | Case Acerto",
    page_icon=str(RESOURCES_DIR.joinpath("logo_2.png")),
    layout="wide",
)

st.title("Dados utilizados")

with st.sidebar:
    "[Planejamento](https://docs.google.com/document/d/1KjYd8HR94FH1ZMoEWxI6SCZ_lVyIvGIF_7jPZDHtk9c/edit?usp=sharing)"
    "[Apresentação](https://docs.google.com/presentation/d/1SwAivlGW-JY7K1KCBE56eMsO9HwCef_oI5Y4f8OcEds/edit?usp=sharing)"
    "[Repositório](https://github.com/ewerthonk/ai-assistant-debt)"

st.dataframe(data=df, hide_index=True)
