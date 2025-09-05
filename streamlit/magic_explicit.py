import streamlit as st

# Magic
"**This shows with magic!**"
import pandas as pd
df = pd.DataFrame({'A': [1,2,3]})
df

# Explicit
st.write("**This shows with explicit command!**")
st.dataframe(df)