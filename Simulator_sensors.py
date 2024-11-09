import paho.mqtt.client as mqtt
import random
import time
import configparser
import threading

# Load MQTT configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

client_address = config['mqtt']['client_address']
port = int(config['mqtt']['port'])

greenhouses = int(config['data_generation']['greenhouses'])
zones = int(config['data_generation']['zones'])
time_sleep = int(config['data_generation']['time_sleep'])
sensors = config['data_generation']['sensors'].split('|')

mqtt_client = mqtt.Client()
mqtt_client.connect(client_address, port=port)

# Function to publish zone data to MQTT broker
def publish_zone_data(mqtt_client, sensors, greenhouse, zone):
    while True:
        # Generate random sensor data
        for sensor in sensors:
            if sensor == 'temperature':
                data = round(random.uniform(18, 30), 2)  # Simulating temperature in Celsius for a greenhouse
            elif sensor == 'humidity':
                data = round(random.uniform(40, 80), 2)  # Simulating humidity percentage for optimal plant growth
            elif sensor == 'soil_moisture':
                data = round(random.uniform(20, 60), 2)  # Simulating soil moisture percentage
            elif sensor == 'light_intensity':
                data = random.randint(200, 1000)  # Simulating light intensity in lumens
            elif sensor == 'co2':
                data = random.randint(400, 800)  # Simulating CO2 concentration in ppm for plant photosynthesis
            topic = f"{sensor}/greenhouse_{greenhouse}/zone_{zone}"
            mqtt_client.publish(topic, f'{{"{sensor}":{data}}}')
            print(f"Published {topic}: {data}")

        time.sleep(time_sleep)  # Delay between data publications

# Start threads for each greenhouse zone
threads = []
for greenhouse in range(greenhouses):
    for zone in range(zones):
        thread = threading.Thread(target=publish_zone_data, args=(mqtt_client, sensors, greenhouse, zone))
        threads.append(thread)
        thread.start()

# Optionally, join threads if needed (not usually required as the loops are infinite)
# for thread in threads:
#     thread.join()
