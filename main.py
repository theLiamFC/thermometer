import Thermometer
import myWifi

from machine import Pin, PWM, ADC
import math
import time
import utime

# Connect to Wifi
myWifi.connect(myWifi.TUFTS)

# Motor initiation
dirPin = Pin(14,Pin.OUT)
stepPin = Pin(15,Pin.OUT)
theTherm = Thermometer.Thermometer(stepPin, dirPin)

# Thermistor initiation
thermistor = ADC(28)
kMvAvg = []

def thermTemp(res):
    k = 1/((math.log(res / 34963) / -2860) + (1/298))
    
    kMvAvg.append(k)
    if len(kMvAvg) > 10:
        kMvAvg.pop(0)
    kAvg = sum(kMvAvg) / len(kMvAvg)
    
    c = kAvg - 273.1
    f = (c * 9/5) + 32
    
    return c,f

# LED initiation
led = PWM(Pin(16,Pin.OUT))
led.freq(1000)

for i in range(20):
    c,f = thermTemp(thermistor.read_u16())
    theTherm.moveTemp(f,'f')
    print(f)
    time.sleep(2)
    
theTherm.home()

