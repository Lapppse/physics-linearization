import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from utils import Functions
from utils.enums import PlotType


class Plot:
    def __init__(self, df: pd.DataFrame, plot_type: PlotType):
        self.plot_type = plot_type
        self.df = df
        self.df_drop = df.dropna()
        self.update()

    def update(self):
        self._update_fig()
        self._update_x()
        self._update_axes()
        self._update_plot()
        self.draw()
        self._update_legend()

    def draw(self):
        st.plotly_chart(self.fig)

    def _update_fig(self):
        self.fig = go.Figure()
        self.fig.add_trace(
            go.Scatter(
                x=self.df_drop["x"], y=self.df_drop["y"], mode="markers", name="Points"
            ),
        )
        self.fig.update_traces(marker=dict(size=10))

    def _update_x(self):  # FIXME: naming
        self.x_max = self.df["x"].max()
        match self.plot_type:
            case PlotType.LINEAR:
                reg = LinearRegression()
                reg.fit(self.df_drop.loc[:, ["x"]], self.df_drop.loc[:, ["y"]])
                self.slope, self.intercept = (reg.coef_[0][0], reg.intercept_[0])

                self.x_min = (self.intercept * -1) / self.slope
                self.x_min = (
                    min(1, self.x_min) if self.slope < 0 else max(1, self.x_min)
                )
            case PlotType.SEMILOG:
                self.slope, self.intercept = np.polyfit(
                    self.df_drop["x"], np.log(self.df_drop["y"]), 1
                )
                self.x_min = 1
            case PlotType.LOG:
                reg = LinearRegression()
                reg.fit(
                    np.log(self.df_drop.loc[:, ["x"]]),
                    np.log(self.df_drop.loc[:, ["y"]]),
                )
                self.slope, self.intercept = (
                    reg.coef_[0][0],
                    np.exp(reg.intercept_[0]),
                )

                self.x_min = 1

    def _update_axes(self):
        match self.plot_type:
            case PlotType.LINEAR:
                self.fig.update_yaxes(type="linear")
                self.fig.update_xaxes(type="linear")
            case PlotType.SEMILOG:
                self.fig.update_yaxes(type="log")
                self.fig.update_xaxes(type="linear")
            case PlotType.LOG:
                self.fig.update_yaxes(type="log")
                self.fig.update_xaxes(type="log")

    def _update_plot(self):
        match self.plot_type:
            case PlotType.LINEAR:
                self.fig.add_trace(
                    go.Scatter(
                        x=(self.x_min, self.x_max),
                        y=Functions.linear(
                            (self.x_min, self.x_max),
                            self.slope,
                            self.intercept,
                        ),
                        mode="lines",
                        name="Linear regression",
                    )
                )
            case PlotType.SEMILOG:
                self.fig.add_trace(
                    go.Scatter(
                        x=(self.x_min, self.x_max),
                        y=Functions.exponential(
                            (self.x_min, self.x_max),
                            self.slope,
                            self.intercept,
                        ),
                        mode="lines",
                        name="Exponential regression",
                    )
                )
            case PlotType.LOG:
                self.fig.add_trace(
                    go.Scatter(
                        x=(self.x_min, self.x_max),
                        y=Functions.power(
                            (self.x_min, self.x_max),
                            self.slope,
                            self.intercept,
                        ),
                        mode="lines",
                        name="Power regression",
                    )
                )

    def _update_legend(self):
        match self.plot_type:
            case PlotType.LINEAR:
                st.markdown(
                    f"Linear regression on transformed data: y = {round(self.slope, 3)}x + {round(self.intercept, 3)}"
                )
            case PlotType.SEMILOG:
                st.markdown(
                    f"Exponential regression on transformed data: ln(y) = {self.slope:.3f}x + {self.intercept:.3f}"
                )
            case PlotType.LOG:
                st.markdown(
                    f"Power regression on transformed data: y = {round(self.intercept, 3)} · x<sup>{round(self.slope, 3)}</sup>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"Mean squared error {
                            round(mean_absolute_error(self.df["y"], Functions.power(self.df["x"], self.slope, self.intercept)), 3)
                            }"
                )
