#!/usr/bin/env python3

import serial
import time
import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port: {port.device}")
        print(f"  Description: {port.description}")
        print(f"  HWID: {port.hwid}")
        print()

def read_sensor_data(port, baudrate):
    try:
        # Open serial port
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Listening on {port} at {baudrate} baud rate...")

        while True:
            # Read data from the serial port
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"Received data: {data}")

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        # Close the serial port
        if ser.is_open:
            ser.close()
            print(f"Closed {port}")

if __name__ == "__main__":
    # Adjust the port and baud rate as necessary
    port = '/dev/cu.usbmodem0000000000001'  # Replace with the correct port for your system
    baudrate = 9600        # Match the baud rate of your IoT device

    read_sensor_data(port, baudrate)
    # list_serial_ports()
