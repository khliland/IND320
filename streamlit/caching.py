import streamlit as st

@st.cache_data
def get_data():
    import time; time.sleep(2) # Simulate expensive task
    return [1, 2, 3]

st.write("Data:", get_data())

# Interactive part that costs very little compute time
if 'counter' not in st.session_state:
    st.session_state.counter = 0

def increment():
    st.session_state.counter += 1

st.button("Increment", on_click=increment)
st.write(f"Button clicked {st.session_state.counter} times")