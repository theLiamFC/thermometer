import time

class Thermometer(object):
    def __init__(self, stepPin, dirPin):
        self.step = stepPin
        self.dirPin = dirPin
        self.loc = 0
        self.CCW = False
        self.CW = True
        
    def moveTo(self, dest, delay):
        while dest != self.loc:
            if dest > self.loc:
                self.dirPin.value(self.CCW)
                self.step.value(1)
                time.sleep(0.003)
                self.step.value(0)
                time.sleep(0.003)
                self.loc += 1
            elif dest < self.loc:
                self.dirPin.value(self.CW)
                self.step.value(1)
                time.sleep(0.003)
                self.step.value(0)
                time.sleep(0.003)
                self.loc -= 1
            time.sleep(delay)
            
    def moveTemp(self,temp,unit):
        if unit == "f":
            dest = int(1.16*temp - 3.08)
        elif unit == "c":
            dest = 200 + int(1.16*temp - 3.08)
        self.moveTo(dest,0.003)
        
    def home(self):
        self.moveTo(0,0.003)
