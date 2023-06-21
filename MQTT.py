import time
import ubinascii
import machine
from machine import Pin
import dht
#import ujson
from umqtt.simple import MQTTClient

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER ="io.adafruit.com"
PORT = 1883
ADAFRUIT_USERNAME = "Emil1985"
ADAFRUIT_PASSWORD ="aio_wsoG467HbPIK5hqlDV5wakSKvVtI"
TEMPERATURE_TOPIC = b"Emil1985/feeds/temperature-and-humidity.temperature"
HUMIDITY_TOPIC = b"Emil1985/feeds/temperature-and-humidity.humidity"
publish_interval=60
last_publish=time.time()


def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def get_temperature_and_humidity():
    sensor = dht.DHT11(Pin(27))
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return(temp,hum)

def start_mqtt():
    print(f"Starting connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
    mqttClient.connect()
    print(f"Connected to MQTT Broker :: {MQTT_BROKER}")

    while True:

        global last_publish

        if(time.time() - last_publish) >= publish_interval:
            temp_and_humidity = get_temperature_and_humidity()
            temp = temp_and_humidity[0]
            humidity = temp_and_humidity[1]

           # Not used - created two feeds instead
           # temp_and_humidity = ujson.dumps(temp_and_humidity)
           
            mqttClient.publish(TEMPERATURE_TOPIC, str(temp))
            mqttClient.publish(HUMIDITY_TOPIC, str(humidity))
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
