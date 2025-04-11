import time
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    # port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=10
)

def arm(g, h):
    ser.write(g.encode())
    time.sleep(h)
