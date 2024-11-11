import paho.mqtt.client as mqtt
import configparser
import time
import threading
import importlib

# Load MQTT configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

client_address = config['mqtt']['client_address']
port = int(config['mqtt']['port'])

greenhouses = int(config['data_generation']['greenhouses'])
habitats = int(config['data_generation']['habitats'])
time_sleep = int(config['data_generation']['time_sleep'])
sensors = config['data_generation']['sensors'].split('|')

mqtt_client = mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Specify the MQTT protocol version
mqtt_client.connect(client_address, port=port)

# Dynamically import sensor generation functions
sensor_functions = {}
for sensor in sensors:
    try:
        # Import the module dynamically from the sensors directory
        sensor_module = importlib.import_module(f'{sensor}_sensor')
        
        # Assuming each sensor module has a function named `generate_<sensor>_data`
        function_name = f'generate_{sensor}_data'
        
        # Retrieve the function and add it to the sensor_functions dictionary
        sensor_functions[sensor] = getattr(sensor_module, function_name)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading sensor '{sensor}': {e}")

# Function to publish habitat data to MQTT broker
def publish_habitat_data(mqtt_client, sensors, greenhouse, habitat):
    while True:
        # Generate and publish sensor data
        for sensor in sensors:
            data_function = sensor_functions.get(sensor)
            if data_function:
                data = data_function()
                topic = f"{sensor}/greenhouse_{greenhouse}/habitat_{habitat}"
                mqtt_client.publish(topic, f'{{"{sensor}":{data}}}')
                print(f"Published {topic}: {data}")
        
        time.sleep(time_sleep)  # Delay between data publications

# Start threads for each greenhouse habitat
threads = []
for greenhouse in range(greenhouses):
    for habitat in range(habitats):
        thread = threading.Thread(target=publish_habitat_data, args=(mqtt_client, sensors, greenhouse, habitat))
        threads.append(thread)
        thread.start()

# Optionally, join threads if needed (not usually required as the loops are infinite)
# for thread in threads:
#     thread.join()
