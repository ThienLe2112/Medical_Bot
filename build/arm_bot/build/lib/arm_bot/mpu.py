import smbus			#import SMBus module of I2C
import time
import math
bus = smbus.SMBus(1)
def read_raw_data(DeviceAddress, addr):
        #Accelerometer and Gyroscope's values have 16 bit.

        high = bus.read_byte_data(DeviceAddress, addr)
        low = bus.read_byte_data(DeviceAddress, addr+1)

        #concat values
        values = ((high << 8) | low)
        
        #bit 15 is sign bit
        if values>32768:
            values = values-65536
        return values

class mpu6050():
    def __init__(self, 
                 DeviceAddress = 0x68):
        # super().__init__()
        self.DeviceAddress = DeviceAddress   # MPU6050 device address
        # Set up power management
        bus.write_byte_data(DeviceAddress, 0x6B, 0x00)

    def gyro_signals(self):
        DeviceAddress = self.DeviceAddress

        
        #Swith on the low pass filter
        bus.write_byte_data(DeviceAddress, 0x1A, 0x05)
        
        #Configure the accelerometer output, setting full-scale range at 8g
        bus.write_byte_data(DeviceAddress, 0x1C, 0x10)
        # time.sleep(1)
        #Pull the accelerometer measurements from the sensor
        AccXLSB = read_raw_data(DeviceAddress, 0x3B)
        AccYLSB = read_raw_data(DeviceAddress, 0x3D)
        AccZLSB = read_raw_data(DeviceAddress, 0x3F)

        #Configure the gyroscope
        bus.write_byte_data(DeviceAddress, 0x1B, 0x08)
        # time.sleep(1)
        #Pull the gyroscope measurements from the sensor

        GyroX = read_raw_data(DeviceAddress, 0x43)
        GyroY = read_raw_data(DeviceAddress, 0x45)
        GyroZ = read_raw_data(DeviceAddress, 0x47)
        
        # print(GyroX)
        # print(GyroY)
        # print(GyroZ)
        RateRoll = float(GyroX)/65.5
        RatePitch = float(GyroY)/65.5
        RateYaw = float(GyroZ)/65.5

        AccX = float(AccXLSB)/4096 - 0.17
        AccY = float(AccYLSB)/4096 - 0.030
        AccZ = float(AccZLSB)/4096 - 0.03

        AngleRoll = math.atan(AccY/math.sqrt(math.pow(AccX,2) + math.pow(AccZ,2)))*1/(3.142/180)
        AnglePitch = math.atan(-AccX/math.sqrt(math.pow(AccY,2) + math.pow(AccZ,2)))*1/(3.142/180)
        return AccX, AccY, AccZ, AngleRoll, AnglePitch, RateRoll, RatePitch, RateYaw
    
    

if __name__ == "__main__":
    # time.sleep(250)
    bus.write_byte_data(DeviceAddress, 0x6B, 0x00)

    while True:
        AccX, AccY, AccZ, AngleRoll, AnglePitch, RateRoll, RatePitch, RateYaw = gyro_signals()
        # print("Acceleration X [g] = {%.2f}" % AccX, end='')
        # print("Acceleration Y [g] = {%.2f}" % AccY, end='')
        # print("Acceleration Z [g] = {%.2f}" % AccZ)
        print("Roll Angle: {%.2f}" % AngleRoll, end='')
        print("Pitch Angle: {%.2f}" % AnglePitch)
        time.sleep(0.05)