import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import paho.mqtt.client as mqtt
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

output_quene = Queue(2)
servoes = {
    "servo0": 0,
    "servo1": 0,
    "servo2": 0,
    "servo3": 0,
    "servo4": 0,
    "servo5": 0,
    }
key_save = {
    "KEY_W": 0,
    "KEY_S": 0,
    "KEY_A": 0,
    "KEY_D": 0
    }
control = {
    "P0": 1500,
    "P1": 1500,
    "P2": 1500,
    "P3": 1500,
    "P4": 1500,
    "P5": 1500
    }


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
            if False:
            # if 'sensors' in data.keys():
                #Control servo
                AR = data["sensors"]["MPU0"]["Angle_Roll"]
                AP = data["sensors"]["MPU0"]["Angle_Pitch"]
                RY = data["sensors"]["MPU0"]["Rate_Yaw"]
                AR1 = data["sensors"]["MPU1"]["Angle_Roll"]
                AP1 = data["sensors"]["MPU1"]["Angle_Pitch"]
                RY1 = data["sensors"]["MPU1"]["Rate_Yaw"]
                grip = data["sensors"]["LC"]["force"]
                self.wakeup = 1
            elif not output_quene.empty():
                AR = data["mpu0"]["AR"]
                AP = data["mpu0"]["AP"]
                RY = data["mpu0"]["RY"]
                AR1 = data["mpu1"]["AR"]
                AP1 = data["mpu1"]["AP"]
                RY1 = data["mpu1"]["RY"]
                grip = data["force"]
                self.wakeup = 1
            if self.wakeup == 1:
                self.wakeup = 0
                if RY1 > 4 or RY1 < -4:
                    self.control["P0"] += RY1
                self.control["P1"] = 2500*(-AP+120)/(90 + 90)
                self.control["P3"] = 2500*(-AP1*2+90)/(90 + 90)
                if self.control["P3"] < 0:
                    self.control["P2"] = 1500 + self.control["P3"]
                self.control["P4"] = 2500*(+AR1+90)/(90 + 90)
                self.control["P5"] = 1300 + int(955*grip/0.2)*1.2

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


def on_message(client,userdata,message):
    fields=message.payload.decode()
    data=json.loads(str(fields))
    # if output_quene.full():
    #     output_quene.get()
    #     output_quene.get()

    # output_quene.put(fields)
    # if not output_quene.empty():
    AR = data["mpu1"]["AR"]
    AP = data["mpu1"]["AP"]
    RY = data["mpu1"]["RY"]
    AR1 = data["mpu2"]["AR"]
    AP1 = data["mpu2"]["AP"]
    RY1 = data["mpu2"]["RY"]
    grip = data["force"]
    


    if RY1 > 4:
        control["P0"] += RY1*0.3
    if RY1 < -10:
        control["P0"] += RY1*0.3
    control["P1"] = 2500*(-AP+120)/(90 + 90)
    control["P3"] = 2500*(-AP1*2+90)/(90 + 90)
    if control["P3"] < 0:
        control["P2"] = 1500 + control["P3"]
    control["P4"] = 2500*(+AR1+90)/(90 + 90)
    control["P5"] = 1300 + int(955*grip/0.2)*1.2

    control["P0"] = sorted((500, control["P0"], 2300))[1]
    control["P1"] = sorted((200, control["P1"], 1500))[1]
    control["P2"] = sorted((200, control["P2"], 2300))[1]
    control["P3"] = sorted((200, control["P3"], 1400))[1]
    control["P4"] = sorted((200, control["P4"],2300))[1]
    control["P5"] = sorted((1500,control["P5"],2000))[1]


    servoes["servor1"] = int(control["P0"])
    servoes["servor2"] = int(control["P1"])
    servoes["servor3"] = int(control["P2"])
    servoes["servor4"] = int(control["P3"])
    servoes["servor5"] = int(control["P4"])
    servoes["servor6"] = int(control["P5"])

    msg = String()
    msg_data = json.dumps(servoes).encode()
    client.publish("AllServors",msg_data)
    # fields = output_quene.get()
    # print(fields)

def on_connect(client, userdata,flags,rc):
    print("Connected with result code {}".format(rc))
    client.subscribe('AllSensors')
    
def on_disconnect(client,userdata,rc):
    print("Disconnected from Broker")

# def mqtt_subscribe():
    # client_id='tbi2'
    # client =mqtt.Client(client_id)
    # client.on_connect=on_connect
    # client.on_disconnect=on_disconnect
    # client.on_message=on_message
    # client.username_pw_set(username='thietbi02',password='thietbi02')
    # client.connect("192.168.7.105",1883,60)
    # client.loop_forever()

executor = ThreadPoolExecutor(max_workers=2)

def main(args=None):
    # client_id='tbi1'
    client =mqtt.Client('control2')
    client.on_connect=on_connect
    client.on_disconnect=on_disconnect
    client.on_message=on_message
    client.username_pw_set(username='control',password='control')
    client.connect("192.168.7.105",1883,60)
    client.loop_forever()
    # rclpy.init(args=args)
    # process = executor.submit(mqtt_subscribe)

    # sense_info_subscriber = SensInfoSubscriber()

    # rclpy.spin(sense_info_subscriber)

    # sense_info_subscriber.destroy_node()
    # rclpy.shutdown()


if __name__ == '__main__':
    # client_id='tbi1'
    # client =mqtt.Client(client_id)
    # client.on_connect=on_connect
    # client.on_disconnect=on_disconnect
    # client.on_message=on_message
    # client.username_pw_set(username='thietbi1',password='thietbi1')
    # client.connect("127.0.0.1",1883,60)
    # client.loop_forever()
    main()
    
