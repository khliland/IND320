import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import pandas as pd
from shapely.geometry import shape, Point

st.set_page_config(page_title="Price Areas", layout="wide")
st.title("Choropleth + Single Click Pin")

# Data (adjust to your geojson)
@st.cache_data
def load_geojson():
    with open("../No_sync/2025 CA/price_areas.geojson") as f:
        return json.load(f)

geojson_data = load_geojson()

# Find correct name for area
@st.cache_data
def build_id_to_name(gj):
    out = {}
    for f in gj.get("features", []):
        fid = f.get("id") or (f.get("properties") or {}).get("id")
        if fid is None:
            continue
        name = (f.get("properties") or {}).get("ElSpotOmr")
        if name:
            out[fid] = str(name)
    return out

id_to_name = build_id_to_name(geojson_data)

# Build shapely polygons once (session cache)
if "polygons" not in st.session_state:
    polys = []
    for feat in geojson_data.get("features", []):
        fid = feat.get("id") or (feat.get("properties") or {}).get("id")
        if not fid:
            continue
        try:
            geom = shape(feat["geometry"])
        except Exception:
            continue
        polys.append((fid, geom))
    st.session_state.polygons = polys

def find_feature_id(lon: float, lat: float):
    if shape is None or "polygons" not in st.session_state:
        return None
    pt = Point(lon, lat)  # shapely uses (x,y) = (lon,lat)
    for fid, geom in st.session_state.polygons:
        if geom.covers(pt):  # boundary-inclusive
            return fid
    return None

# Choropleth values (example; replace with real data)
value_map = {6: 5.0, 7: 3.5, 8: 4.2, 9: 6.1, 10: 2.8}
df_vals = pd.DataFrame({"id": list(value_map.keys()), "value": list(value_map.values())})

# Session state init
if "last_pin" not in st.session_state:
    st.session_state.last_pin = [66.32624933088354, 14.186465980232347]
if "selected_feature_id" not in st.session_state:
    st.session_state.selected_feature_id = None

# Preselect area for the initial pin (no click required)
if st.session_state.selected_feature_id is None:
    lat, lon = st.session_state.last_pin
    st.session_state.selected_feature_id = find_feature_id(lon, lat)

# Layout: map left, info right
map_col, info_col = st.columns([2.2, 1])

with map_col:
    # Build map (one per run)
    m = folium.Map(location=st.session_state.last_pin, zoom_start=5, tiles="OpenStreetMap")

    # Choropleth (single layer)
    folium.Choropleth(
        geo_data=geojson_data,
        data=df_vals,
        columns=["id", "value"],
        key_on="feature.id",
        fill_color="YlGnBu",
        fill_opacity=0.4,
        line_opacity=0.8,
        line_color="white",
        legend_name="Value",
        highlight=True
    ).add_to(m)

    # Highlight the selected polygon outline (pre-filtered; no filter_function)
    if st.session_state.selected_feature_id is not None:
        sel_id = st.session_state.selected_feature_id
        sel_feats = [
            f for f in geojson_data.get("features", [])
            if f.get("id") == sel_id or (f.get("properties") or {}).get("id") == sel_id
        ]
        if sel_feats:
            folium.GeoJson(
                {"type": "FeatureCollection", "features": sel_feats},
                style_function=lambda f: {"fillOpacity": 0, "color": "red", "weight": 3},
                name="selection"
            ).add_to(m)

    # Single pin (last clicked)
    folium.Marker(
        location=st.session_state.last_pin,
        icon=folium.Icon(color="red"),
        popup=f"{st.session_state.last_pin[0]:.5f}, {st.session_state.last_pin[1]:.5f}"
    ).add_to(m)

    # Render (width inherits from column)
    out = st_folium(m, key="choropleth_map", height=600, width=None)

    # Process click: update pin and polygon ID, then single rerun
    if out and out.get("last_clicked"):
        lat = out["last_clicked"]["lat"]
        lon = out["last_clicked"]["lng"]
        new_coord = [lat, lon]
        if new_coord != st.session_state.last_pin:
            st.session_state.last_pin = new_coord
            st.session_state.selected_feature_id = find_feature_id(lon, lat)
            st.rerun()

with info_col:
    st.subheader("Selection")
    st.write(f"Lat: {st.session_state.last_pin[0]:.6f}")
    st.write(f"Lon: {st.session_state.last_pin[1]:.6f}")

    if st.session_state.selected_feature_id is None:
        st.write("Outside known features.")
    else:
        fid = st.session_state.selected_feature_id
        # If your value_map uses int keys and fid is str, this handles both
        try:
            val = value_map.get(fid, value_map.get(int(fid), "n/a"))
        except Exception:
            val = value_map.get(fid, "n/a")
        area_name = id_to_name.get(fid, f"ID {fid}")
        st.write(f"Area: {area_name}")
        st.write(f"Value: {val}")
