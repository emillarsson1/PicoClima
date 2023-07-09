import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import sensors

# Insert MQTT information below
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER ="io.adafruit.com"
PORT = 1883
ADAFRUIT_USERNAME = "USERNAME HERE"
ADAFRUIT_PASSWORD ="PASSWORD HERE"
TEMPERATURE_TOPIC = b"TEMPERATURE TOPIC HERE"
HUMIDITY_TOPIC = b"HUMIDITY TOPIC HERE"
SOIL_TEMPERATURE_TOPIC=b"SOIL TEMPERATURE TOPIC HERE"
SOIL_HUMIDITY_TOPIC=b"SOIL HUMIDITY TOPIC HERE"

# Set the publish interval (in seconds)
publish_interval=600
last_publish=time.time()

# Function that will reset the hardware if needed
def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

# Connect to the MQTT broker

    def start_mqtt():
        print(f"Starting connection with MQTT Broker :: {MQTT_BROKER}")
        mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=700)
        try:
            mqttClient.connect()
            print(f"Connected to MQTT Broker :: {MQTT_BROKER}")
        
        # Reset the Raspberry Pi Pico W if the connection failed
        except OSError:
                print("Failed to connect to MQTT Broker, resetting...")
                reset()

        # Loop for publishing to the MQTT broker starts here
        while True:

            global last_publish
        
            # Check if it is time to publish according to the set interval
            if(time.time() - last_publish) >= publish_interval:
        
            # Get the indoor temperature and humidity and save the two values in a list
            temp_and_humidity = sensors.get_temperature_and_humidity()
            
            # Get the soil temperature and humidity and save the two values in a list
            temp_and_moisture = sensors.get_soil_temperature_and_humidity()
            
            # Save the temp and humidity in two different variables
            temp = temp_and_humidity[0]
            humidity = temp_and_humidity[1]
            
            # Save the soil temp and humidity in two different variables
            soil_temp=temp_and_moisture[0]
            soil_moisture=temp_and_moisture[1]

            # Publish to the four different feeds
            mqttClient.publish(TEMPERATURE_TOPIC, str(temp))
            mqttClient.publish(HUMIDITY_TOPIC, str(humidity))
            mqttClient.publish(SOIL_TEMPERATURE_TOPIC, str(soil_temp))
            mqttClient.publish(SOIL_HUMIDITY_TOPIC, str(soil_moisture))
            
            # Set the last publish time to the current time
            last_publish=time.time()
            
            # Get current time and change it to a readable format
            local_time = time.localtime()
            date_time_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            local_time[0],  # year
            local_time[1],  # month
            local_time[2],  # day
            local_time[3],  # hour
            local_time[4],  # minute
            local_time[5]   # second
            )
            
            # Print out confirmation that the data was sent
            print("The data was sent at " + str(date_time_str))
            
        # Wait 10 seconds
        time.sleep(10)
