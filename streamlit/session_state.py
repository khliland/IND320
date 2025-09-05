import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

def increment():
    st.session_state.counter += 1

st.button("Increment", on_click=increment)
st.write(f"Button clicked {st.session_state.counter} times")