import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import sensors

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER ="io.adafruit.com"
PORT = 1883
ADAFRUIT_USERNAME = "USERNAME HERE"
ADAFRUIT_PASSWORD ="PASSWORD HERE"
TEMPERATURE_TOPIC = b"TEMPERATURE TOPIC HERE"
HUMIDITY_TOPIC = b"HUMIDITY TOPIC HERE"
SOIL_TEMPERATURE_TOPIC=b"SOIL TEMPERATURE TOPIC HERE"
SOIL_HUMIDITY_TOPIC=b"SOIL HUMIDITY TOPIC HERE"

publish_interval=60
last_publish=time.time()

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def start_mqtt():
    print(f"Starting connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
    mqttClient.connect()
    print(f"Connected to MQTT Broker :: {MQTT_BROKER}")

    while True:

        global last_publish

        if(time.time() - last_publish) >= publish_interval:
            temp_and_humidity = sensors.get_temperature_and_humidity()
            temp_and_moisture = sensors.get_soil_temperature_and_humidity()
            
            temp = temp_and_humidity[0]
            humidity = temp_and_humidity[1]
            
            soil_temp=temp_and_moisture[0]
            soil_moisture=temp_and_moisture[1]

            mqttClient.publish(TEMPERATURE_TOPIC, str(temp))
            mqttClient.publish(HUMIDITY_TOPIC, str(humidity))
            mqttClient.publish(SOIL_TEMPERATURE_TOPIC, str(soil_temp))
            mqttClient.publish(SOIL_HUMIDITY_TOPIC, str(soil_moisture))
            
            last_publish=time.time()
            local_time = time.localtime()
            date_time_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            local_time[0],  # year
            local_time[1],  # month
            local_time[2],  # day
            local_time[3],  # hour
            local_time[4],  # minute
            local_time[5]   # second
            )
            print("The data was sent at " + str(date_time_str))
            

        time.sleep(10)
