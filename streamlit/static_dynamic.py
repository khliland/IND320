import streamlit as st

# Static Example
st.markdown("# Static Dashboard\nThis content won't change until the file is reloaded.")

# Dynamic Example
user_input = st.text_input("Type something:")
if user_input:
    st.write(f"You entered: {user_input}")