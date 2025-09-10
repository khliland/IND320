import streamlit as st

# Static Example
st.markdown("# Static Flashboard\nThis content won't change until the file is reloaded again.")

# Dynamic Example
user_input = st.text_input("Type something:")
if user_input:
    st.write(f"You entered: {user_input}")