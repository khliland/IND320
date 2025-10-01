# mongodb.py

import streamlit as st
import pymongo

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"])

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client['example']
    collection = db['data']
    items = collection.find()
    items = list(items)
    return items

items = get_data()

# Print results.
for item in items:
    st.write(f"{item['name']} is {item['age']} years old")