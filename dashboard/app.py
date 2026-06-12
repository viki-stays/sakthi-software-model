from mqtt_subscriber import latest_data

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import folium
from streamlit_folium import st_folium
import json
import os

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="SAKTHI Dashboard",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="sakthi_refresh"
)

st.title("🌾 SAKTHI Control Dashboard")
# MQTT Debug Panel
st.subheader("📡 Live MQTT Data")

st.json(latest_data)
# ======================================
# LOAD WAYPOINTS
# ======================================

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
# LOAD FARM BOUNDARY GEOJSON
# ======================================

FARM_FILE = os.path.join(
    BASE_DIR,
    "Field.geojson"
)

with open(FARM_FILE, "r") as f:
    farm_geojson = json.load(f)
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
# DISEASE DETECTION RESULT
# ======================================

disease_status = True

disease_name = "Potato Early Blight"

confidence = 92.53

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
    location=[11.639, 78.093],
    zoom_start=16
)

# ======================================
# FARM BOUNDARY
# ======================================

folium.GeoJson(
    farm_geojson,
    name="Farm Boundary",
    style_function=lambda x: {
        "color": "green",
        "weight": 3,
        "fillColor": "green",
        "fillOpacity": 0.15
    }
).add_to(m)

path = [

[11.6340,78.0840],
[11.6430,78.0840],

[11.6430,78.0860],
[11.6340,78.0860],

[11.6340,78.0880],
[11.6430,78.0880],

[11.6430,78.0900],
[11.6340,78.0900],

[11.6340,78.0920],
[11.6430,78.0920],

[11.6430,78.0940],
[11.6340,78.0940],

[11.6340,78.0960],
[11.6430,78.0960],

[11.6430,78.0980],
[11.6340,78.0980],

[11.6340,78.1000],
[11.6430,78.1000]

]
folium.PolyLine(
    path,
    color="blue",
    weight=4,
    popup="Lawnmower Path"
).add_to(m)
# ======================================
# ROVER POSITION
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
    [11.639, 78.093],
        popup=f"{disease_name} ({confidence:.2f}%)",
        icon=folium.Icon(
            color="red"
        )
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

st.subheader("🌱 Disease Alert")

if disease_status:

    st.error(
        f"{disease_name} Detected\n\nConfidence: {confidence:.2f}%"
    )

else:

    st.success(
        "No Disease Detected"
    )

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
        f"Disease: {disease_name}"
    )

    st.write(
        f"Confidence: {confidence:.2f}%"
    )

    st.write(
        "Navigation Mode: Autonomous"
    )

    st.write(
        "Path Type: Lawnmower Coverage"
    )
