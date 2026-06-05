import streamlit as st

st.set_page_config(page_title="SAKTHI Dashboard")

st.title("🌾 SAKTHI Control Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Battery", "78%")

with col2:
    st.metric("Waypoint", "12")

with col3:
    st.metric("Speed", "0.8 m/s")

st.divider()

st.subheader("Current Task")
st.success("Monitoring Row 3")

st.subheader("Disease Alert")
st.info("No disease detected")

st.subheader("Irrigation Advisory")
st.warning("Skip watering today")
