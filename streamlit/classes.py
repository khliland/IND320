import numpy as np
import plotly.graph_objects as go
import streamlit as st
from numpy.random import default_rng as rng
from scipy.stats import gaussian_kde

class DensityChartApp:
    """Render a density chart for three deterministic random data groups."""

    group_labels = ["Group A", "Group B", "Group C"]
    group_offsets = [-3, 0, 3]

    def create_hist_data(self) -> list[np.ndarray]:
        return [
            rng(seed).standard_normal(200) + offset
            for seed, offset in enumerate(self.group_offsets)
        ]

    def create_figure(self) -> go.Figure:
        figure = go.Figure()

        for data, label in zip(self.create_hist_data(), self.group_labels):
            density = gaussian_kde(data)
            x_values = np.linspace(data.min(), data.max(), 200)
            figure.add_trace(
                go.Scatter(
                    x=x_values,
                    y=density(x_values),
                    mode="lines",
                    fill="tozeroy",
                    name=label,
                )
            )

        return figure

    def run(self) -> None:
        st.plotly_chart(self.create_figure())

class NotInitializedClass:
    """This class is not initialized and should not be run."""

    def create_large_dataframe(self) -> np.ndarray:
        return np.random.randn(100000, 100000) # Overflows memory

    def run(self) -> None:
        raise RuntimeError("This class should not be run.")

DensityChartApp().run()