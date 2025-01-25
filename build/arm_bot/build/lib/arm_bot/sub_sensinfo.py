import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class SensInfoSubscriber(Node):
	def __init__(self):
		super().__init__('sense_info_subscriber')
		self.subscription = self.create_subscription(
			String,
			'sensors',
			self.listener_callback,
			10)
		self.subscription

	def listener_callback(self, msg):
		data = json.loads(msg.data)
		keyboard = data["keyboard"]
		sensors = data["sensors"]
		self.get_logger().info('keyboard: {keyboard}, Data2: {sensors}')
		
def main(args=None):
	rclpy.init(args=args)

	sense_info_subscriber = SensInfoSubscriber()

	rclpy.spin(sense_info_subscriber)

	sense_info_subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
