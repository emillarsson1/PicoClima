import dht
import seesaw
import stemma_soil_sensor

from machine import Pin, I2C

''' 
Function that retrieves indoor humidity and temperature
from the DHT11 sensor
'''

def get_temperature_and_humidity():
    sensor = dht.DHT11(Pin(27))
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return(temp,hum)

'''
Function that retrieves soil moisture and temperature
from the Adafruit STEMMA soil sensor
'''

def get_soil_temperature_and_humidity():
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))
    SENSOR_ADDR = 0x36
    seesaw2 = stemma_soil_sensor.StemmaSoilSensor(i2c)
    moisture = seesaw2.get_moisture()
    temperature = seesaw2.get_temp()
    return(temperature,moisture)
