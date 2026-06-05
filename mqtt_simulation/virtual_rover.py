import json
import time
import random
import ssl
import paho.mqtt.client as mqtt

BROKER = "8566ab19a88f457bbf19d434e33a739c.s1.eu.hivemq.cloud"

USERNAME = "Sakthi"
PASSWORD = "123456789qW"

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
    8883
)

print("Connected to HiveMQ")

while True:

    data = {
        "lat": round(12.9716 + random.uniform(-0.00005,0.00005),6),
        "lon": round(77.5946 + random.uniform(-0.00005,0.00005),6),
        "battery": random.randint(40,100),
        "status": "monitoring"
    }

    client.publish(
        "sakthi/location",
        json.dumps(data)
    )

    print(data)

    time.sleep(5)
