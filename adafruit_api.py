from Adafruit_IO import MQTTClient
import sys
from uart import Uart
class Adafruit_API:
    def __init__(self,username,key,feed_id_list,port = None):
        self.username = username
        self.feed_id_list = feed_id_list
        self.key = key
        self.mqtt_client = None
        self.uart = None
        self.port = port
    def connected(self,client):
        print("Connected to server!")
        for feed_id in self.feed_id_list:
            print("Subscribe to " + feed_id)
            client.subscribe(feed_id)
    def subscribe(self,client,userdata, mid , granted_qos):
        print("Subscribe successful!")
    def disconnected(client):
        print("Disconnect succcessful!")
        sys.exit(1)
    def message(self,client,feed_id,payload):
        print("Receive from " + feed_id + " : " + payload)

        if feed_id == 'led':
            if payload == '1':
                print("Turn on light")
                self.uart.write_message("A")
            if payload == '0':
                print("Turn off light")
                self.uart.write_message("B")
        if feed_id == 'door':
            if payload == '1':
                print("Open door")
                self.uart.write_message("D")
            if payload == '0':
                print("Close door")
                self.uart.write_message("E")
        if feed_id == 'fan':
            print("C")
            self.uart.write_message("C")
        if feed_id == 'air-conditioner':
            print("C"+payload)
            self.uart.write_message("C"+payload)
        if feed_id == 'led-changer':
            print("F"+payload)
            self.uart.write_message("F"+payload)
    def publish(self,feed_id,data):
        print("Publish to " + feed_id + " : " + str(data))
        self.mqtt_client.publish(feed_id,data)
    def connect(self):
        self.mqtt_client = MQTTClient(self.username,self.key)
        self.mqtt_client.on_connect = self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message
        self.mqtt_client.on_subscribe = self.subscribe
        self.mqtt_client.connect()
        if (self.port != None):
            self.uart = Uart(self.port,self)
            self.uart.init_connection()
            self.mqtt_client.loop_background()
    def read_serial(self):
        self.uart.read_serial()