from mqtt_subscriber import latest_data

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import folium
from streamlit_folium import st_folium
import json

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="SAKTHI Dashboard",
    layout="wide"
)

# Auto refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="sakthi_refresh"
)

st.title("🌾 SAKTHI Control Dashboard")

# Debug (remove later if needed)
st.write("Live MQTT Data:", latest_data)

# ======================================
# LOAD WAYPOINTS
# ======================================
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

WAYPOINT_FILE = os.path.join(
    BASE_DIR,
    "path_planning",
    "waypoints.json"
)

with open(WAYPOINT_FILE, "r") as f:
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
# LIVE MQTT DATA
# ======================================

battery = latest_data["battery"]

index = latest_data["waypoint"]

rover_position = [
    latest_data["lat"],
    latest_data["lon"]
]

status = latest_data["status"]

# ======================================
# TOP METRICS
# ======================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🔋 Battery",
        f"{battery}%"
    )

with col2:
    st.metric(
        "📍 Waypoint",
        str(index)
    )

with col3:
    st.metric(
        "🚜 Speed",
        "0.8 m/s"
    )

# ======================================
# MAP
# ======================================

m = folium.Map(
    location=rover_position,
    zoom_start=18
)

# ======================================
# FARM BOUNDARY
# ======================================

farm_boundary = [
    [12.9716,77.5946],
    [12.9718,77.5946],
    [12.9718,77.5949],
    [12.9716,77.5949],
    [12.9716,77.5946]
]

folium.Polygon(
    farm_boundary,
    color="green",
    fill=True,
    fill_opacity=0.2,
    popup="Farm Boundary"
).add_to(m)

# ======================================
# PLANNED PATH
# ======================================

folium.PolyLine(
    path,
    color="blue",
    weight=5,
    popup="Generated Coverage Path"
).add_to(m)

# ======================================
# LIVE ROVER POSITION
# ======================================

folium.Marker(
    rover_position,
    popup=f"SAKTHI Rover - WP {index}",
    icon=folium.Icon(
        color="blue",
        icon="info-sign"
    )
).add_to(m)

# ======================================
# DISEASE ALERT MARKER
# ======================================

if disease_status:

    folium.Marker(
        path[-1],
        popup=disease_name,
        icon=folium.Icon(color="red")
    ).add_to(m)

# ======================================
# DISPLAY MAP
# ======================================

st.subheader("🗺️ Live Farm Map")

st_folium(
    m,
    width=1200,
    height=550
)

# ======================================
# CURRENT STATUS
# ======================================

st.subheader("🤖 Current Task")

if status == "MISSION":

    st.success(
        "MISSION IN PROGRESS"
    )

elif status == "RETURNING_TO_BASE":

    st.warning(
        "RETURNING TO BASE"
    )

elif status == "CHARGING":

    st.info(
        "CHARGING"
    )

else:

    st.write(status)

# ======================================
# BATTERY ALERT
# ======================================

if battery < 25:

    st.error(
        "⚠ LOW BATTERY DETECTED"
    )

# ======================================
# DISEASE ALERT PANEL
# ======================================

if disease_status:
    st.error(f"{disease_name} Detected")
else:
    st.success("No Disease Detected")
# ======================================
# IRRIGATION ADVISORY
# ======================================

st.subheader("💧 Irrigation Advisory")

st.warning(
    "Skip Watering Today"
)

# ======================================
# MISSION DETAILS
# ======================================

with st.expander("📊 Mission Details"):

    st.write(
        f"Current Waypoint: {index}"
    )

    st.write(
        f"Battery Level: {battery}%"
    )

    st.write(
        f"Status: {status}"
    )

    st.write(
        "Navigation Mode: Autonomous"
    )

    st.write(
        "Path Type: Lawnmower Coverage"
    )
