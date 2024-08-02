import time
import imu
from machine import Pin, I2C, Timer

bus = I2C(1, scl=Pin(15), sda=Pin(14))
imu = imu.IMU(bus)

stop_flag = False  # Flag to signal stop


def read_imu(t):
    if stop_flag:
        t.stop()  # Stop the Timer
        return
    print(
        "{:>.f},{:>.f},{:>.f}".format(*imu.accel())
        + ","
        + "{:>.f},{:>.f},{:>.f}".format(*imu.gyro())
    )


def stop_recording():
    global stop_flag
    stop_flag = True


imu_timer = Timer(1, period=10000, mode=Timer.PERIODIC, callback=read_imu)
imu_timer.start()

try:
    while not stop_flag:
        time.sleep(1)  # Keep running until stop_flag is set
except KeyboardInterrupt:
    stop_recording()  # Handle stop signal
