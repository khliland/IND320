import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page title and layout
st.set_page_config(
    page_title="Thank You!",
    layout="wide",
)

st.title("Data Visualization")

# Retrieve the name and color from session state
name = st.session_state.get("user_name", "Guest")
color = st.session_state.get("user_color", "#808080")  # Default to gray if not found

# Create a sample DataFrame for the histogram
data = pd.DataFrame(np.random.randn(50, 1), columns=["Value"])

# Create a Plotly histogram with the chosen color
fig = px.histogram(
    data,
    x="Value",
    nbins=10,
    title="Sample Histogram",
    color_discrete_sequence=[color]
)

# Display the histogram
st.plotly_chart(fig, use_container_width=True)

# Display a personalized thank you message
st.markdown(f"**Thank you for your choice, {name}!**")