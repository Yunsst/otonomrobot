import serial
import time



asdasd = serial.Serial('/dev/ttyAMA0', 9600)
time.sleep(2)
asdasd.reset_output_buffer()
while True:
        if (asdasd.in_waiting>0):
                yaw = asdasd.readline().decode('ASCII').rstrip("\n")
                print(yaw)
        else:
                yaw = asdasd.readline().decode('ASCII').rstrip("\n")
                print(yaw)