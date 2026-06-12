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

path = [
    [11.4315,78.7925],
    [11.4370,78.7860],
    [11.4375,78.7865],
    [11.4320,78.7930],
    [11.4325,78.7935],
    [11.4380,78.7870],
    [11.4385,78.7875],
    [11.4330,78.7940]
]

# ======================================
# LIVE MQTT DATA
# ======================================

battery = latest_data["battery"]

index = latest_data["waypoint"]

status = latest_data["status"]

rover_position = [
    latest_data["lat"],
    latest_data["lon"]
]
st.write("Rover Position:", rover_position)
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
    location=[11.437, 78.790],
    zoom_start=15
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
    [11.4315,78.7925],
    [11.4370,78.7860],

    [11.4375,78.7865],
    [11.4320,78.7930],

    [11.4325,78.7935],
    [11.4380,78.7870],

    [11.4385,78.7875],
    [11.4330,78.7940]
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
    [11.435, 78.791],
    popup=f"{disease_name} ({confidence:.2f}%)",
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
