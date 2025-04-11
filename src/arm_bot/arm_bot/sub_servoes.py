import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
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

class ServoSubscriber(Node):
	def __init__(self):
		arm(f'#1P1500#2P1500#3P1500#4P1500#5P1500T100D1\r\n',0.001)
		print("Running servores....")
		time.sleep(5)
		super().__init__('servo_subscriber')
		self.subscription = self.create_subscription(
			String,
			'servoes',
			self.listener_callback,
			10)
		self.subscription

	def listener_callback(self, msg):
		control = json.loads(msg.data)
		P0 = int(control["P0"])
		P1 = int(control["P1"])
		P2 = int(control["P2"])
		P3 = int(control["P3"])
		P4 = int(control["P4"])
		P5 = int(control["P5"])
		arm(f'#1P{P0}#2P{P1}#3P{P2}#4P{P3}#5P{P4}#6P{P5}T100D10\r\n',0.01)
		self.get_logger().info(f'#1P{P0}#2P{P1}#3P{P2}#4P{P3}#5P{P4}#6P{P5}\r\n')
		
def main(args=None):
	rclpy.init(args=args)

	servo_subscriber = ServoSubscriber()

	rclpy.spin(servo_subscriber)

	servo_subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
