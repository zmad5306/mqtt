import random
# import Adafruit_DHT
import json
import datetime
from dotenv import load_dotenv
import os

from paho.mqtt import client as mqtt_client

load_dotenv()

# DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

broker = os.getenv('BROKER_HOST')
port = int(os.getenv('BROKER_PORT'))
username = os.getenv('BROKER_USERNAME')
password = os.getenv('BROKER_PASSWORD')
topic = "environmentals/basic"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    # humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    humidity = 30
    temperature = 70
    timestamp = datetime.datetime.now().replace(second=0).replace(microsecond=0).replace(microsecond=0)
    if humidity is not None and temperature is not None:
        msg = {'sensor_id': 1, 'timestamp': timestamp, 'temperature': temperature, 'humidity': humidity}
        json_msg = json.dumps(msg, default=str)
        print(f"the json is: {json_msg}")
        result = client.publish(topic, json_msg)
        status = result[0]
        if status != 0:
            print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
