import json
import time
import ssl
import paho.mqtt.client as mqtt

# =====================================
# HIVE MQ SETTINGS
# =====================================

BROKER = "8566ab19a88f457bbf19d434e33a739c.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "Sakthi"
PASSWORD = "123456789qW"

# =====================================
# MQTT CLIENT
# =====================================

client = mqtt.Client()

client.username_pw_set(
    USERNAME,
    PASSWORD
)

client.tls_set(
    tls_version=ssl.PROTOCOL_TLS
)

client.connect(
    BROKER,
    PORT
)

client.loop_start()

print("✅ Connected to HiveMQ")

# =====================================
# ROVER PATH
# =====================================

path = [
    [11.4410, 78.7869],
    [11.4436, 78.7852],

    [11.4433, 78.7850],
    [11.4408, 78.7867],

    [11.4406, 78.7865],
    [11.4430, 78.7848],

    [11.4427, 78.7846],
    [11.4404, 78.7863]
]
print("FIRST WAYPOINT =", path[0])
HOME_INDEX = 0

# =====================================
# INITIAL STATE
# =====================================

battery = 100
index = 0

status = "MISSION"

saved_waypoint = None

# =====================================
# MAIN LOOP
# =====================================

while True:

    # ---------------------------------
    # LOW BATTERY CHECK
    # ---------------------------------

    if battery < 25 and status == "MISSION":

        saved_waypoint = index

        print("\n⚠ LOW BATTERY DETECTED")
        print(f"Saving Waypoint: {saved_waypoint}")

        status = "RETURNING_TO_BASE"

        client.publish(
            "sakthi/status",
            status
        )

        # Move rover to home

        print("🏠 Returning To Base")

        index = HOME_INDEX

        lat, lon = path[index]

        data = {
            "lat": lat,
            "lon": lon,
            "battery": battery,
            "status": status,
            "waypoint": index
        }

        client.publish(
            "sakthi/location",
            json.dumps(data)
        )

        time.sleep(5)

        # Charging phase

        status = "CHARGING"

        client.publish(
            "sakthi/status",
            status
        )

        print("🔋 Charging...")

        time.sleep(5)

        battery = 100

        print("✅ Fully Charged")

        status = "MISSION"

        client.publish(
            "sakthi/status",
            status
        )

        index = saved_waypoint

        print(
            f"🚜 Resuming Mission From Waypoint {saved_waypoint}"
        )

    # ---------------------------------
    # NORMAL MISSION
    # ---------------------------------

    lat, lon = path[index]

    data = {
        "lat": lat,
        "lon": lon,
        "battery": battery,
        "status": status,
        "waypoint": index
    }

    payload = json.dumps(data)

    # MQTT Topics

    client.publish(
        "sakthi/location",
        payload
    )

    client.publish(
        "sakthi/battery",
        str(battery)
    )

    client.publish(
        "sakthi/status",
        status
    )

    print("\n------------------------")
    print(f"Waypoint : {index}")
    print(f"Battery  : {battery}%")
    print(f"Status   : {status}")
    print("------------------------")

    # Battery Drain

    battery -= 10

    # Next Waypoint

    index += 1

    if index >= len(path):
        index = 0

    time.sleep(5)
