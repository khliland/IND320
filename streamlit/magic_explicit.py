import streamlit as st

# Magic
"**This shows with magic!**"
import pandas as pd
df = pd.DataFrame({'A': [1,2,3]})
# Show my DataFrame with magic command
df 

# Explicit
st.write("**This shows with explicit command!**")
st.dataframe(df)