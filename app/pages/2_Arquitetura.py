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
    layout="wide",
)
st.title("Arquitetura")
st.image(str(RESOURCES_DIR.joinpath("diagram.png")), width=1100)