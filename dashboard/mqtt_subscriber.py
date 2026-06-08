import json
import ssl
import paho.mqtt.client as mqtt

latest_data = {
    "lat": 12.9716,
    "lon": 77.5946,
    "battery": 100,
    "status": "MISSION",
    "waypoint": 0
}

BROKER = "8566ab19a88f457bbf19d434e33a739c.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "Sakthi"
PASSWORD = "123456789qW"

def on_message(client, userdata, msg):
    global latest_data

    try:
        payload = json.loads(
            msg.payload.decode()
        )

        latest_data = payload

        print("Received:", latest_data)

    except Exception as e:
        print(e)

client = mqtt.Client()

client.username_pw_set(
    USERNAME,
    PASSWORD
)

client.tls_set(
    tls_version=ssl.PROTOCOL_TLS
)

client.on_message = on_message

client.connect(
    BROKER,
    PORT
)

client.subscribe(
    "sakthi/location"
)

client.loop_start()
