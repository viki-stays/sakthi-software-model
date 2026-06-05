import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(page_title="SAKTHI Dashboard")

st.title("🌾 SAKTHI Control Dashboard")

# -------------------------------
# LOAD WAYPOINTS
# -------------------------------

with open("path_planning/waypoints.json") as f:
    waypoints = json.load(f)

# -------------------------------
# CONVERT WAYPOINTS TO MAP COORDS
# -------------------------------

base_lat = 12.9716
base_lon = 77.5946

path = []

for x, y in waypoints:
    lat = base_lat + y * 0.00001
    lon = base_lon + x * 0.00001
    path.append([lat, lon])

# -------------------------------
# ROVER SIMULATION
# -------------------------------

index = int(time.time() / 3) % len(path)

rover_position = path[index]

battery = max(100 - index * 5, 20)

# -------------------------------
# DASHBOARD METRICS
# -------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Battery", f"{battery}%")

with col2:
    st.metric("Waypoint", str(index))

with col3:
    st.metric("Speed", "0.8 m/s")

# -------------------------------
# CREATE MAP
# -------------------------------

m = folium.Map(
    location=[12.9717, 77.5947],
    zoom_start=18
)

# -------------------------------
# FARM BOUNDARY
# -------------------------------

farm_boundary = [
    [12.9716, 77.5946],
    [12.9718, 77.5946],
    [12.9718, 77.5949],
    [12.9716, 77.5949],
    [12.9716, 77.5946]
]

folium.Polygon(
    farm_boundary,
    color="green",
    fill=True,
    fill_opacity=0.2,
    popup="Farm Boundary"
).add_to(m)

# -------------------------------
# GENERATED PATH
# -------------------------------

folium.PolyLine(
    path,
    color="blue",
    weight=4,
    popup="Generated Coverage Path"
).add_to(m)

# -------------------------------
# ROVER MARKER
# -------------------------------

folium.Marker(
    rover_position,
    popup=f"SAKTHI Rover - WP {index}",
    icon=folium.Icon(color="blue")
).add_to(m)

# -------------------------------
# DISEASE ALERT MARKER
# -------------------------------

folium.Marker(
    path[-1],
    popup="Disease Detected",
    icon=folium.Icon(color="red")
).add_to(m)

# -------------------------------
# DISPLAY MAP
# -------------------------------

st.subheader("🗺️ Live Farm Map")

st_folium(
    m,
    width=900,
    height=500
)

# -------------------------------
# TASK STATUS
# -------------------------------

st.subheader("Current Task")

st.success(f"Moving to Waypoint {index}")

# -------------------------------
# DISEASE ALERT PANEL
# -------------------------------

st.subheader("Disease Alert")

disease_status = False

if disease_status:
    st.error("Leaf Blight detected")
else:
    st.success("No disease detected")

# -------------------------------
# IRRIGATION ADVISORY
# -------------------------------

st.subheader("Irrigation Advisory")

st.warning("Skip watering today")

# -------------------------------
# DEBUG INFO
# -------------------------------

with st.expander("Mission Details"):
    st.write(f"Total Waypoints: {len(path)}")
    st.write(f"Current Waypoint: {index}")
    st.write(f"Battery Level: {battery}%")
