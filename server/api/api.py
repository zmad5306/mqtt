from flask import Flask
import os
import psycopg2
import json

app = Flask(__name__)

@app.route("/readings/<string:sensor_id>")
def readings(sensor_id):
    database = os.environ['DB_DATABASE']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_host = os.environ['DB_HOST']
    db_port = int(os.environ['DB_PORT'])

    readings = []

    with psycopg2.connect(database=database, user=db_user, password=db_password, host=db_host, port=db_port) as connection:
        with connection.cursor() as cursor:
            parameters = (sensor_id)
            cursor.execute("select ts, temperature, humidity from readings where sensor_id = %s order by ts", parameters)
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            for row in rows:
                readings.append(dict(zip(colnames, row)))

    return json.dumps(readings, default=str), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)