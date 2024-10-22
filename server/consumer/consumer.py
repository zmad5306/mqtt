import random
import psycopg2
import json
from paho.mqtt import client as mqtt_client
import os


broker = os.environ['MQTT_BROKER_HOST']
port = int(os.environ['MQTT_BROKER_PORT'])
topic = "environmentals/basic"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = os.environ['MQTT_USER']
password = os.environ['MQTT_PASSWORD']

database = os.environ['DB_DATABASE']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_port = int(os.environ['DB_PORT'])


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        reading = json.loads(msg.payload.decode())

        with psycopg2.connect(database=database, user=db_user, password=db_password, host=db_host, port=db_port) as connection:
            with connection.cursor() as cur:
                parameters = (reading['sensor_id'], reading['timestamp'], reading['temperature'], reading['humidity'])
                cur.execute("insert into readings (sensor_id, ts, temperature, humidity) values(%s, %s, %s, %s)", parameters)
                connection.commit()
                
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
