import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="My First Streamlit App",
    layout="wide",
)

st.title("Welcome to My App")
st.write("Please enter your name and choose your favorite color.")

# Define color options
color_options = {
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Purple": "#800080",
    "Orange": "#FFA500",
}

# Drop-down menu for color selection
selected_color_name = st.selectbox("Choose a color:", list(color_options.keys()))

# Display the chosen color - this is outside the form so it updates immediately
st.markdown("Your chosen color is:")
st.markdown(f'<div style="background-color:{color_options[selected_color_name]}; height:50px; width:100%;"></div>', unsafe_allow_html=True)

# Use a form to group the name input and the submit button
with st.form(key='my_form'):
    # Input for the user's name
    name = st.text_input("Enter your name:")
    
    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# Check if the form was submitted
if submit_button:
    if name:
        # Store name and color in session state
        st.session_state["user_name"] = name
        st.session_state["user_color"] = color_options[selected_color_name]
        
        # Navigate to the second page
        st.switch_page("pages/plot.py")
    else:
        st.warning("Please enter your name before submitting.")