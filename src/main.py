import pandas as pd
import streamlit as st

import utils
from elements import *
from utils.enums import *

st.set_page_config(layout="wide")
st.title("Physics Linearization")
col1, col2 = st.columns([1, 3])

utils.init_session_state()

with col1:
    input_selector = selects.InputSelector()
    data_input = DataInput()

with col2:
    plot = Plot(st.session_state.df, st.session_state.plot_type)
    st.markdown(
        f"Correlation: {st.session_state.df['x'].corr(st.session_state.df['y']):.10f}"
    )
    plot_selector = selects.PlotSelector()
