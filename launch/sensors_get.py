from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
            # Node(
            #     package='arm_bot',
            #     namespace='BanDao1',
            #     executable='talker',
            #     name='NhieuChuyen1'
            #       ),
            # Node(
            #     package='arm_bot',
            #     namespace='BanDao1',
            #     executable='listener',
            #     name='NgheNhieu1'
            # ),
			# Node(
            #     package='arm_bot',
            #     namespace='SensorInfo',
            #     executable='keyboard',
            #     name='Keyboard'
            #       ),
            Node(
                package='arm_bot',
                namespace='SensorInfo',
                executable='sensors',
                name='Sensors'
            ),
            Node(
                package='arm_bot',
                namespace='SensorInfo',
                executable='sens_info',
                name='Sensors_Read'
            ),
            # Node(
            #     package='arm_bot',
            #     namespace='Servoes',
            #     executable='servoes',
            #     name='Servoes'
            # ),
          ])
