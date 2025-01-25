import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class MinimalSubscriber(Node):
	def __init__(self):
		super().__init__('minimal_subscriber')
		self.subscription = self.create_subscription(
			String,
			'topic',
			self.listener_callback,
			10)
		self.subscription

	def listener_callback(self, msg):
		data = json.loads(msg.data)
		data1 = int(data["data1"])
		data2 = int(data["data2"])
		self.get_logger().info('Data1: %d, Data2: %d' % (data1,data2))
		
def main(args=None):
	rclpy.init(args=args)

	minimal_subscriber = MinimalSubscriber()

	rclpy.spin(minimal_subscriber)

	minimal_subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
