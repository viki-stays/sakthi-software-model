
import paho.mqtt.client as mqtt
import ssl
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import folium
from streamlit_folium import st_folium
import json
import os
if "latest_data" not in st.session_state:

    st.session_state.latest_data = {
        "lat": 11.44225,
        "lon": 78.78820,
        "battery": 100,
        "status": "MISSION",
        "waypoint": 0
    }
def on_message(client, userdata, msg):

    try:

        payload = json.loads(
            msg.payload.decode()
        )

        st.session_state.latest_data.update(payload)

    except Exception as e:

        print("MQTT Error:", e)
if "mqtt_started" not in st.session_state:

    client = mqtt.Client()

    client.username_pw_set(
        "Sakthi",
        "123456789qW"
    )

    client.tls_set(
        tls_version=ssl.PROTOCOL_TLS
    )

    client.on_message = on_message

    client.connect(
        "8566ab19a88f457bbf19d434e33a739c.s1.eu.hivemq.cloud",
        8883
    )

    client.subscribe(
        "sakthi/location"
    )

    client.loop_start()

    st.session_state.mqtt_started = True
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
st.error("APP VERSION ALAVU")
# MQTT Debug Panel
st.subheader("📡 Live MQTT Data")

st.json(st.session_state.latest_data)
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
# ======================================
# LOAD GEOJSON FARM
# ======================================

FARM_FILE = os.path.join(
    BASE_DIR,
    "alavu.geojson"
)

with open(FARM_FILE, "r") as f:
    farm_geojson = json.load(f)

path = [
    [11.44225, 78.78820],
    [11.44355, 78.78595],

    [11.44320, 78.78570],
    [11.44190, 78.78795],

    [11.44155, 78.78770],
    [11.44285, 78.78545],

    [11.44250, 78.78520],
    [11.44120, 78.78745]
]
# ======================================
# LIVE MQTT DATA
# ======================================

data = st.session_state.latest_data

battery = data.get("battery", 100)

index = data.get("waypoint", 0)

status = data.get("status", "MISSION")

rover_position = [
    data.get("lat", path[0][0]),
    data.get("lon", path[0][1])
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
    location=[11.4425, 78.7865],
    zoom_start=18
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
    [11.4422, 78.7860],
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
st.json(
    st.session_state.latest_data
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
