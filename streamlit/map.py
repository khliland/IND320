import pandas as pd
import plotly.express as px
import streamlit as st

# Local restaurants and cafes
restaurants = pd.read_csv('../D2Dbook/data/restaurants.csv')

fig_restaurants = px.scatter_map(
    restaurants,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data=["type","lat","lon"],
    color_discrete_sequence=["green"],
    # Size of sequence
    size=[10]*len(restaurants),
    size_max=8,
    zoom=14,
    height=600,
    width=700,
)
fig_restaurants.update_layout(mapbox_style="open-street-map")
fig_restaurants.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# If "restaurant" is not in the session state, initialize it
st.title("Local Restaurants and Cafes")

st.plotly_chart(fig_restaurants, key = "restaurant", on_select="rerun", use_container_width=False)
st.subheader("")
st.subheader("Clicked Restaurant Info")
if st.session_state["restaurant"]:
    st.json(st.session_state["restaurant"])