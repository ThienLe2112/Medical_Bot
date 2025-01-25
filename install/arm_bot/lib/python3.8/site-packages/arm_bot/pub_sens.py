import rclpy
from rclpy.node import Node
from std_msgs.msg import String 
import json
from arm_bot.mpu import mpu6050

class SensPublisher(Node):
    def __init__(self):
        super().__init__('sens_publisher')
        self.publisher_ = self.create_publisher(String, 'sensors', 10)
        timer_period = 0.01 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.MPU0 = mpu6050(DeviceAddress = 0x68)
        self.sens = {
            "sensors":{
                "MPU0":{
                    "Angle_Roll": 0,
                    "Angle_Pitch": 0,
                    "Angle_Yaw": 0
                },
                "MPU1":{
                    "Angle_Roll": 0,
                    "Angle_Pitch": 0,
                    "Angle_Yaw": 0
                },
                "MPU2":{
                    "Angle_Roll": 0,
                    "Angle_Pitch": 0,
                    "Angle_Yaw": 0
                },
                "VL053":{
                    "Distance": 0
                }
            }
        }
    def timer_callback(self):
        #update MPU0's values:
        AccX, AccY, AccZ, AngleRoll, AnglePitch = self.MPU0.gyro_signals()
        self.sens["sensors"]["MPU0"]["Angle_Roll"] = AngleRoll
        self.sens["sensors"]["MPU0"]["Angle_Pitch"] = AnglePitch
        
        msg = String()

        msg.data = json.dumps(self.sens)
        self.publisher_.publish(msg)
        self.get_logger().info('Sens\tSend: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    
    sens_publisher = SensPublisher()

    rclpy.spin(sens_publisher)
    
    sens_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
