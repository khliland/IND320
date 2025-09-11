# Import streamlit
import streamlit as st

# Add a header to the app
st.header("A strange and complicated Streamlit app")

# Add a button with a label
if st.button("Press me!"):
    st.write("You pressed the button!")

# Add a slider with a range from 0 to 100 in increments of 2, starting at 50
slider_num = st.slider("Select a value", 0, 100, value=50, step=2)
st.write("Slider value:", slider_num)