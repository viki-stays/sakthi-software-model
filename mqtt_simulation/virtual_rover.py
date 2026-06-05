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
    [12.97160, 77.59460],
    [12.97162, 77.59462],
    [12.97164, 77.59464],
    [12.97166, 77.59466],
    [12.97168, 77.59468],
    [12.97170, 77.59470],
    [12.97172, 77.59472],
    [12.97174, 77.59474]
]

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
