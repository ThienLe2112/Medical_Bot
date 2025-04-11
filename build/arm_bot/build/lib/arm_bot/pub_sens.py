import rclpy
from rclpy.node import Node
from std_msgs.msg import String 
import json
from arm_bot.mpu import mpu6050
from arm_bot.load_cell import get_force
import time
import serial


class SensPublisher(Node):
    def __init__(self):
        super().__init__('sens_publisher')
        self.publisher_ = self.create_publisher(String, 'sensors', 10)
        self.i = 1
        timer_period = 0.001 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.MPU0 = mpu6050(DeviceAddress = 0x68)
        self.MPU1 = mpu6050(DeviceAddress = 0x69)
        self.sens = {
            "sensors":{
                "MPU0":{
                    "Angle_Roll": 0,
                    "Angle_Pitch": 0,
                    "Rate_Yaw": 0
                },
                "MPU1":{
                    "Angle_Roll": 0,
                    "Angle_Pitch": 0,
                    "Rate_Yaw": 0
                },
                "LC":{
                    "force": 0
                },
                "VL053":{
                    "Distance": 0
                }
            }
        }
        self.start = 2
        self.lc = ''
        self.grip = 0
        
        self.serial_port = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            
        )
    def timer_callback(self):
        # update MPU0's values:
        AX, AY, AZ, AR, AP, RR, RP, RY = self.MPU0.gyro_signals()
        AX1, AY1, AZ1, AR1, AP1, RR1, RP1, RY1 = self.MPU1.gyro_signals()

        if self.serial_port.inWaiting() > 0:
            # data = self.serial_port.read().decode("utf-8")
            data = self.serial_port.read().decode("ISO-8859-1")
        #     print(data)
            if str(data) == "*" and self.start == 1:
                    self.start = 0
                    self.grip=(float(self.lc))
                    self.serial_port.flushInput()
                    self.lc = ''
            elif self.start == 1:
                    self.lc += str(data)
            elif str(data) == "#":
                    self.start = 1 

        self.sens["sensors"]["MPU0"]["Angle_Roll"] = AR
        self.sens["sensors"]["MPU0"]["Angle_Pitch"] = AP
        self.sens["sensors"]["MPU0"]["Rate_Yaw"] = RY
        self.sens["sensors"]["MPU1"]["Angle_Roll"] = AR1
        self.sens["sensors"]["MPU1"]["Angle_Pitch"] = AP1
        self.sens["sensors"]["MPU1"]["Rate_Yaw"] = RY1
        self.sens["sensors"]["LC"]["force"] = self.grip

        msg = String()

        msg.data = json.dumps(self.sens)
        self.publisher_.publish(msg)
        self.get_logger().info('Sens\tSend: "%s"' % msg.data)
        # self.get_logger().info(f'{grip, self.start}')
        # time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    
    sens_publisher = SensPublisher()

    rclpy.spin(sens_publisher)
    
    sens_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
