import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="SAKTHI Dashboard")

st.title("🌾 SAKTHI Control Dashboard")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Battery","78%")

with col2:
    st.metric("Waypoint","12")

with col3:
    st.metric("Speed","0.8 m/s")

# Create Map

m = folium.Map(
    location=[12.9716,77.5946],
    zoom_start=18
)

# Rover Marker

folium.Marker(
    [12.9716,77.5946],
    popup="SAKTHI Rover"
).add_to(m)

st.subheader("Live Farm Map")

st_folium(
    m,
    width=900,
    height=500
)

st.subheader("Current Task")
st.success("Monitoring Row 3")

st.subheader("Disease Alert")
st.info("No disease detected")

st.subheader("Irrigation Advisory")
st.warning("Skip watering today")
