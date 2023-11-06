# thermometer
A IOT thermometer device

This repository is for an IOT device that physically displays current temperature 
readings. It also pulls data from the 3rd party server AirTable and posts data
to Adafruit Dashboard. The physical device was made using a Raspberry Pi Pico W,
thermistor, stepper motor, and accelerometer.

The following code files were used in this project.

colorVision.py:
Runs on local PC. Uses OpenCV to threshold and detect blobs of color before
updating the results to AirTable.

main.py:
Runs directly on the Pico. Interfaces with Thermometer, Accelerometer, MQTT,
and urequests libraries.

Thermometer.py:
Runs directly on the Pico. Is a library to manage the stepper motor and the
relationship between steps and degrees.

Accelerometer.py:
Runs directly on the Pico. Is a library to get acceleration, gyroscope, and
temperature data from the LSM6DS3.

MQTT.py
Runs directly on the Pico. Is a public library found here:
https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple

uRequests.py
Runs directly on the Pico. Is a public library downloaded from the Thonny IDE.
