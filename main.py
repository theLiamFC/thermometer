import Thermometer
import myWifi
import accelerometer as accel
#import acgy

from machine import Pin, PWM, ADC
import mqtt
import math
import time
import utime
import urequests as requests

# Connect to Wifi
myWifi.connect(myWifi.HOME)

# Adafruit MQTT Connect
adafruit = mqtt.MQTTClient("itsTherm",
                            server="io.adafruit.com",
                            user=myWifi.AIO_USERNAME,
                            password=myWifi.AIO_KEY,
                            keepalive=600)
adafruit.connect()

# Air Table API Stuff
url = "https://api.airtable.com/v0/apphONQQbp3lZsxcN/Thermometer/rec8VqwIFGb9AMTaP"
headers = {
    "Authorization": "Bearer " + myWifi.AT_TOKEN,
}

# Motor initiation
dirPin = Pin(14,Pin.OUT)
stepPin = Pin(15,Pin.OUT)
theTherm = Thermometer.Thermometer(stepPin, dirPin)

# Thermistor initiation
thermistor = ADC(28)
kMvAvg = []

#led = Pin(16, Pin.OUT)
#led.value(0)
led = PWM(Pin(16))
led.freq(1000)
led.duty_u16(20000)

def thermTemp(res):
    k = 1/((math.log(res / 34963) / -2860) + (1/298))
    
    kMvAvg.append(k)
    if len(kMvAvg) > 10:
        kMvAvg.pop(0)
    kAvg = sum(kMvAvg) / len(kMvAvg)
    
    c = kAvg - 273.1
    f = (c * 9/5) + 32
    
    return c,f

lastTimeAD = time.time() - 301
lastTimeAT = time.time() - 31
ledSince = time.time() - 6
ledIsOn = False

for i in range(500):
    # get thermistor reading
    c,f = thermTemp(thermistor.read_u16())
    print(c,f)
    
    # send MQTT to Adafruit every 5 min
    if (time.time() - lastTimeAD) > 300:
        adafruit.publish('liamfc/feeds/temperature',str(f))
        lastTimeAD = time.time()
        print("published temps via MQTT: ",c,f)
    
    # get temp unit from Air Table every 10 seconds
    if (time.time() - lastTimeAT) > 3:
        reply = requests.get(url, headers=headers)
        unit = reply.json()['fields']['Unit']
        lastTimeAT = time.time()
        print("grabbed unit via API: ",unit)
    print(unit)
    
    # update physical temp display
    if unit == "Fahrenheit":
        theTherm.moveTemp(f,'f')
        print("updated physical display as F")
    elif unit == "Celsius":
        theTherm.moveTemp(c,'c')
        print("updated physical display as C")
    else:
        print("Unrecognized unit")
    
    # update LED based on accelerometer reading
    if ledIsOn and (time.time() - ledSince) > 5:
        print("reset LED")
        #led.value(0)
        led.duty_u16(20000)
        ledIsOn = False
    else:
        totalAccel = (abs(accel.getAccel()[0])+abs(accel.getAccel()[1])+abs(accel.getAccel()[2])) / 3
        if totalAccel > 5000:
            print("high acceleration: ", totalAccel)
            #led.value(1)
            led.duty_u16(60000)
            ledIsOn = True
            ledSince = time.time()
    
    time.sleep(0.1)
    
theTherm.home()
