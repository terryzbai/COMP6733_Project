import time
import imu
from machine import Pin, I2C, Timer

bus = I2C(1, scl=Pin(15), sda=Pin(14))
imu = imu.IMU(bus)

def mycallback(t):
    print('{:>.f},{:>.f},{:>.f}'.format(*imu.accel())+','+'{:>.f},{:>.f},{:>.f}'.format(*imu.gyro()))
    
    
tim = Timer(1, period=10000, mode=Timer.PERIODIC,callback=mycallback)
tim.start()

time.sleep_ms(1000)
tim.stop()
