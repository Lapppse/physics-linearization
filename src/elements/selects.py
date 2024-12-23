import pandas as pd
import streamlit as st

from utils.enums import *


class PlotSelector:
    def __init__(self):
        self.plot_types = (PlotType.LINEAR, PlotType.SEMILOG, PlotType.LOG)
        self.plot_type_selector = st.selectbox(
            "Select plot scale",
            self.plot_types,
            format_func=lambda x: x.value.capitalize(),
            key="plot_type",
        )


class InputSelector:
    def __init__(self):
        self.input_types = (InputType.TABLE, InputType.EXCEL)
        self.selector = st.radio(
            "Data input", 
            self.input_types,
            format_func=lambda type: type.value.capitalize(),
            horizontal=True,
            key="input_type",
        )