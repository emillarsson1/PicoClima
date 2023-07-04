# PicoClima

This project is for a Raspberry Pi Pico W microcontroller connected with a DHT11 sensor and an Adafruit STEMMA soil sensor.

It was created by me, Emil Larsson, as a project for the Introduction to Applied IoT at Linnaeus University in 2023.

To use the code, simply transfer all files to your Raspberry Pi Pico W microcontroller.

Then edit the Adafruit IO settings in MQTT.py, lines 9 to 17. 
You will also need to edit sensors.py so that the pins matches your phsyical connections on the Raspberry Pi Pico W.
