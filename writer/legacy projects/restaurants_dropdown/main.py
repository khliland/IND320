import writer
import pandas as pd
import plotly.express as px

# Its name starts with _, so this function won't be exposed

# Import data
def _get_main_df():
    main_df = pd.read_csv('../../D2Dbook/data/restaurants.csv') 
    return main_df

# Plot restaurants
def _update_plotly_restaurants(state):
    restaurants = state["restaurants_df"]
    selected_num = state["selected_num"]
    sizes = [10]*len(restaurants)
    if selected_num != -1:
        sizes[selected_num] = 20
    fig_restaurants = px.scatter_mapbox(
        restaurants,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data=["type","lat","lon"],
        color_discrete_sequence=["darkgreen"],
        zoom=14,
        height=600,
        width=700,
    )
    overlay = fig_restaurants['data'][0]
    overlay['marker']['size'] = sizes
    fig_restaurants.update_layout(mapbox_style="open-street-map")
    fig_restaurants.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    state["plotly_restaurants"] = fig_restaurants

def handle_click(state, payload):
    restaurants = state["restaurants_df"]
    state["selected"] = restaurants["name"].values[payload[0]["pointNumber"]]
    state["selected_num"] = payload[0]["pointNumber"]
    _update_plotly_restaurants(state)

def handle_choice(state, payload):
    restaurants = state["restaurants_df"]
    state["selected"] = restaurants["name"].values[int(payload)]
    state["selected_num"] = int(payload)
    _update_plotly_restaurants(state)

def _get_JSON(state):
    restaurants = state["restaurants_df"]
    # Create JSON with keys list(range(9)), and restaurant names as values
    my_json = dict(zip(list(range(len(restaurants))), restaurants["name"].values))
    # Convert keys to strings
    my_json = {str(key): value for key, value in my_json.items()}
    print(my_json)
    state["restaurant_JSON"] = my_json
    handle_choice(state, 0)

# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore (not used here)

initial_state = writer.init_state({
    "my_app": {
        "title": "Restaurant selection"
    },
    "_my_private_element": 1337,
    "selected":"Click to select",
    "selected_num":-1,
    "restaurants_df":_get_main_df(),
})

_update_plotly_restaurants(initial_state)
_get_JSON(initial_state)