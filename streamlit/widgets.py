import streamlit as st

value = st.slider("Pick a value", 0, 100, value=24, step=1)
title = st.selectbox("Select title", 
    ("Ms.", "Mrs.", "Mr.", "Dr.", "Prof.", "Lady", "Lord", "Dutchess", "Duke", "Queen", "King", "Master", "Mistress"))
area = st.pills("Select area", ["Ås", "Ski", "Drøbak", "Kroer", "Vestby"], selection_mode="multi")
subject = st.radio("Choose a subject", ["Deployment", "Data Sources", "Data Quality", "Machine Learning"])
check = st.checkbox("Please, check")
active = st.toggle("Agree, or not?", value=True)
# Use st.session_state to make printout conditional
st.write("Chosen")
st.write(value, title, area, subject, check, active)