import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class SensInfoSubscriber(Node):
    def __init__(self):
        super().__init__('sense_info_subscriber')

        # Subscriber
        self.subscription = self.create_subscription(
            String,
            'sensors',
            self.listener_callback,
            10)
        self.subscription

        # Publisher
        self.publisher_ = self.create_publisher(String, 'servoes', 10)
        timer_period = 0.01 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.servoes = {
            "servo0": 0,
            "servo1": 0,
            "servo2": 0,
            "servo3": 0,
            "servo4": 0,
            "servo5": 0,
        }
        self.key_save = {
                "KEY_W": 0,
                "KEY_S": 0,
                "KEY_A": 0,
                "KEY_D": 0
            }
        self.control = {
            "P0": 1500,
            "P1": 1500,
            "P2": 1500,
            "P3": 1500,
            "P4": 1500,
            "P5": 1500
            }
        self.data = dict()
        self.wakeup = 0
    def listener_callback(self, msg):
        data = json.loads(msg.data)
        self.data = data
        if 'keyboard' in data.keys():
            self.wakeup = 1
            keyboard = data["keyboard"]
            self.get_logger().info('keyboard: %s' % data["keyboard"])
        if 'sensors' in data.keys():
            sensors = data["sensors"]
            # self.get_logger().info('sensors: %s' % data["sensors"])
        
    def timer_callback(self):
        if self.wakeup == 0:
            data = self.data
            self.wakeup=0
            if 'sensors' in data.keys():
                #Control servo
                AR = data["sensors"]["MPU0"]["Angle_Roll"]
                AP = data["sensors"]["MPU0"]["Angle_Pitch"]
                RY = data["sensors"]["MPU0"]["Rate_Yaw"]
                AR1 = data["sensors"]["MPU1"]["Angle_Roll"]
                AP1 = data["sensors"]["MPU1"]["Angle_Pitch"]
                RY1 = data["sensors"]["MPU1"]["Rate_Yaw"]

                self.control["P0"]
                if RY1 > 4 or RY1 < -4:
                    self.control["P0"] += RY1
                self.control["P1"] = 2500*(-AP+120)/(90 + 90)
                self.control["P3"] = 2500*(-AP1*2+90)/(90 + 90)
                if self.control["P3"] < 0:
                    self.control["P2"] = 1500 + self.control["P3"]
                self.control["P4"] = 2500*(+AR1+90)/(90 + 90)
                self.control["P5"] = 1500# 1300 + int(955*grip/0.5)*1.2

                self.control["P0"] = sorted((500, self.control["P0"], 2300))[1]
                self.control["P1"] = sorted((200, self.control["P1"], 1500))[1]
                self.control["P2"] = sorted((200, self.control["P2"], 2300))[1]
                self.control["P3"] = sorted((200, self.control["P3"], 1400))[1]
                self.control["P4"] = sorted((200, self.control["P4"],2300))[1]
                self.control["P5"] = sorted((1500,self.control["P5"],2200))[1]


                self.servoes["servo0"] = self.control["P0"]
                self.servoes["servo1"] = self.control["P1"]
                self.servoes["servo2"] = self.control["P2"]
                self.servoes["servo3"] = self.control["P3"]
                self.servoes["servo4"] = self.control["P4"]
                self.servoes["servo5"] = self.control["P5"]

                msg = String()
                msg.data = json.dumps(self.control)
                self.publisher_.publish(msg)
                
                self.get_logger().info('%s' % msg.data)



            



def main(args=None):
    rclpy.init(args=args)

    sense_info_subscriber = SensInfoSubscriber()

    rclpy.spin(sense_info_subscriber)

    sense_info_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
