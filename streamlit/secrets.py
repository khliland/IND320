import streamlit as st

# Assume secrets.toml has a section called 
# [api] 
# where the secret is stored after 
# key =
st.write("API Key:", st.secrets["api"]["second_key"])