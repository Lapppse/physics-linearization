import pandas as pd
import streamlit as st

from .enums import *


def init_session_state():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame({"x": [1.1, 2], "y": [2.2, 4]})
    if "plot_type" not in st.session_state:
        st.session_state.plot_type = PlotType.LINEAR
    if "input_type" not in st.session_state:
        st.session_state.input_type = InputType.TABLE