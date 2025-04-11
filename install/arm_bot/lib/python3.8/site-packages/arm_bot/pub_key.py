import rclpy
from rclpy.node import Node
from std_msgs.msg import String 
import json
from inputs import get_key

class KeyPublisher(Node):
    def __init__(self):
        super().__init__('key_publisher')
        self.publisher_ = self.create_publisher(String, 'sensors', 10)
        timer_period = 0.001 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.key = {
            "keyboard":{
                "KEY_W": 0,
                "KEY_S": 0,
                "KEY_A": 0,
                "KEY_D": 0
            }
        }
    def timer_callback(self):

        events = get_key()
        for event in events:
            if event.ev_type in ["Key"]:
                if event.code in ["KEY_W", "KEY_S", "KEY_A", "KEY_D"]:
                    # print(event.ev_type, event.code, event.state)
                    self.key["keyboard"][event.code] = event.state
                    msg = String()

                    msg.data = json.dumps(self.key)
                    self.publisher_.publish(msg)
                    self.get_logger().info('KEY\tSend: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    
    key_publisher = KeyPublisher()

    rclpy.spin(key_publisher)
    
    key_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
