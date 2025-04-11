import serial


serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    
)

def get_force(sens, start):
    grip = 0
    if serial_port.inWaiting() > 0:
        # data = serial_port.read().decode("utf-8")
        data = serial_port.read().decode("ISO-8859-1")
    #     print(data)
        if str(data) == "*" and start == 1:
                start = 0
                grip=(float(sens))
                serial_port.flushInput()
                sens = ''
        elif start == 1:
                sens += str(data)
        elif str(data) == "#":
                start = 1 
    
        return sens, grip, start
            