# Streamlit app with weather selection using OpenWeatherMap API
import streamlit as st
import requests
import json

API_KEY = open('../No_sync/api_key_OpenWeather','r').read()

# Dropdown for city selection
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Mo i Rana"]
city = st.selectbox("Select a city", cities)
is_selectbox = True

# A search box for city input
city_input = st.text_input("Enter city name", "")
if city_input:
    is_selectbox = False
    city = city_input
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    location_data = json.loads(response.text)
else:
    location_data = ["1"]

# Multi-select buttons for weather properties
properties = ["Temperature", "Humidity", "Weather Description"]
selected_properties = st.multiselect("Select weather properties to display", properties, default=properties)

# Fetch weather data for the selected city
if city:
    if is_selectbox:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    elif len(location_data) > 0:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={location_data[0]['lat']}&lon={location_data[0]['lon']}&appid={API_KEY}"
    if len(location_data) > 0:
        response = requests.get(url)
        weather_data = json.loads(response.text)

    # Display weather information
    if len(location_data) > 0 and weather_data["cod"] == 200:
        st.write(f"Weather in {city}:")
        if "Humidity" in selected_properties:
            st.write(f"Humidity: {weather_data['main']['humidity']}%")
        if "Temperature" in selected_properties:
            st.write(f"Temperature: {weather_data['main']['temp']} K")
        if "Weather Description" in selected_properties:
            st.write(f"Description: {weather_data['weather'][0]['description']}")
    else:
        st.write("City not found.")