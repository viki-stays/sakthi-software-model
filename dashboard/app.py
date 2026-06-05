from mqtt_client import latest_data
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import time

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="SAKTHI Dashboard",
    layout="wide"
)

st.title("🌾 SAKTHI Control Dashboard")

# ======================================
# LOAD WAYPOINTS
# ======================================

with open("path_planning/waypoints.json") as f:
    waypoints = json.load(f)

# ======================================
# CONVERT WAYPOINTS TO MAP COORDINATES
# ======================================

base_lat = 12.9716
base_lon = 77.5946

path = []

for x, y in waypoints:

    lat = base_lat + y * 0.000004
    lon = base_lon + x * 0.0000025

    path.append([lat, lon])

# ======================================
# ROVER SIMULATION
# ======================================

index = int(time.time() / 3) % len(path)

rover_position = [
    latest_data["lat"],
    latest_data["lon"]
]

battery = latest_data["battery"]

# ======================================
# TOP METRICS
# ======================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔋 Battery", f"{battery}%")

with col2:
    st.metric("📍 Waypoint", str(index))

with col3:
    st.metric("🚜 Speed", "0.8 m/s")

# ======================================
# MAP
# ======================================

m = folium.Map(
    location=[12.9717, 77.5947],
    zoom_start=18
)

# ======================================
# FARM BOUNDARY
# ======================================

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

# ======================================
# GENERATED COVERAGE PATH
# ======================================

folium.PolyLine(
    path,
    color="blue",
    weight=5,
    popup="Generated Coverage Path"
).add_to(m)

# ======================================
# ROVER POSITION
# ======================================

folium.Marker(
    rover_position,
    popup=f"SAKTHI Rover - WP {index}",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# ======================================
# DISEASE ALERT LOCATION
# ======================================

folium.Marker(
    path[-1],
    popup="Disease Detected",
    icon=folium.Icon(color="red")
).add_to(m)

# ======================================
# MAP DISPLAY
# ======================================

st.subheader("🗺️ Live Farm Map")

st_folium(
    m,
    width=1200,
    height=550
)

# ======================================
# CURRENT TASK
# ======================================

st.subheader("🤖 Current Task")

if battery < 20:
    st.error("⚠ Low Battery - Return To Base Activated")
else:
    st.success(
    f"Status : {latest_data['status']}"
)

# ======================================
# DISEASE ALERT PANEL
# ======================================

st.subheader("🌱 Disease Alert")

disease_status = False

if disease_status:
    st.error("Leaf Blight Detected")
else:
    st.success("No Disease Detected")

# ======================================
# IRRIGATION ADVISORY
# ======================================

st.subheader("💧 Irrigation Advisory")

st.warning("Skip Watering Today")

# ======================================
# MISSION DETAILS
# ======================================

with st.expander("📊 Mission Details"):

    st.write(f"Total Waypoints: {len(path)}")
    st.write(f"Current Waypoint: {index}")
    st.write(f"Battery Level: {battery}%")
    st.write("Navigation Mode: Autonomous")
    st.write("Path Type: Lawnmower Coverage")
