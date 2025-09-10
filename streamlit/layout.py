import streamlit as st

left, right = st.columns(2, border=True)

with left:
    st.write("This is the left column")
    expander = st.expander("Soo secret")
    expander.write('''
        This is an explanation that is hidden until you click the expander.
    ''')

with right:
    tabA, tabB = st.tabs(["Tab A", "Tab B"])

    tabA.subheader("This is tab A")
    tabA.write("You can put any elements in a tab")

    tabB.subheader("This is tab B")
    tabB.write("You can put any elements in a tab, also here")