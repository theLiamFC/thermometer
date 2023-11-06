#https://www.pololu.com/file/0J1087/LSM6DS33.pdf
#https://github.com/jposada202020/MicroPython_LSM6DSOX/blob/master/micropython_lsm6dsox/lsm6dsox.py

from machine import Pin, I2C
import struct, time

LSM = 0x6A

sclP = 22
sdaP = 21
i2c = I2C(0, scl=Pin(sclP), sda=Pin(sdaP), freq=100000) 
print([hex(i) for i in i2c.scan()])

ID = i2c.readfrom_mem(LSM, 0x0F, 1)
ID = struct.unpack('<b',ID)[0]

rate = {'done': 0b0000,'12.5':0b0001,'26':0b0010,'52':0b0011,'104':0b0100,'208':0b0101,'416':0b0110,'833':0b0111,'1.66k':0b1000,'3.33k':0b1001,'6.66k':0b1010,'1.6':0b1011}
anti_alias = {'400':0b00,'200':0b01,'100': 0b10, '50':0b11}
XL_range = {'2g':0b00,'4g':0b10,'8g':0b11, '16g':0b01}
G_range = {'250':0b00, '500':0b01,'1000':0b10,'2000':0b11}
G_125_fullscale = 0

XLfactor = (0.061, 0.488, 0.122, 0.244)
Gfactor = (8.75, 17.50, 35.0, 70.0)

# 58 = =high performance, +/- 4g
XL = (rate['208']<<4) + (XL_range['4g']<<2) + anti_alias['400']
i2c.writeto_mem(LSM, 0x10, struct.pack('>b',XL)) # enable accel

# 58 = high performance - 1000 dps
G = (rate['1.66k']<<4) + (G_range['1000']<<2) + (G_125_fullscale <<1) + 0
i2c.writeto_mem(LSM, 0x11, struct.pack('>b',G)) # enable gyro

time.sleep(0.2)

def getTemp():
    temp = i2c.readfrom_mem(LSM, 0x20, 2)
    temp = struct.unpack('<h',temp)[0]
    return temp /256 + 25.0

def getGyro():
    gyro = i2c.readfrom_mem(LSM, 0x22, 6)
    return struct.unpack('<hhh',gyro)

def getAccel():
    accel = i2c.readfrom_mem(LSM, 0x28, 6)
    return struct.unpack('<hhh',accel)
