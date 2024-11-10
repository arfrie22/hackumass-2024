import serial
import time

ser = serial.Serial("/dev/cu.usbserial-DN01AZ26", 9600)
   
# Send character 'S' to start the program
ser.write(b'b')  # Write the letter 'b'
ser.write(bytes([1]))  # Write the byte 0x07
ser.write(b'\n')  # Write the byte 0x07

time.sleep(1)

# Read line   
while True:
    bs = ser.readline()
    print(bs)