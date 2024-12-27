from copy import deepcopy

import pandas as pd
import streamlit as st

from utils.enums import InputType


def onchange(df: pd.DataFrame):
    st.session_state.df = df


class DataInput:
    def __init__(self):
        self.df = st.session_state.df
        match st.session_state.input_type:
            case InputType.TABLE:
                with st.form("pd_input_form"):
                    st.session_state.df = st.data_editor(
                        self.df,
                        num_rows="dynamic",
                        use_container_width=True,
                        column_config={
                            "x": st.column_config.NumberColumn(
                                "x", help="x (variable) axis", format="%.10f"
                            ),
                            "y": st.column_config.NumberColumn(
                                "y", help="y (function) axis", format="%.10f"
                            ),
                        },
                    )
                    st.form_submit_button("Submit", on_click=self.update)
            case InputType.EXCEL:
                uploaded_file = st.file_uploader("Choose excel file")
                if uploaded_file:
                    st.session_state.df = pd.read_excel(uploaded_file)

    def update(self):
        st.session_state.df = self.df
