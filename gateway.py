from adafruit_api import Adafruit_API
import time
from threading import Thread
from voice import *
from main import *
def StartVoiceRecognition(client):
    while True:
        start_signal_detect(client)
def EventFaceRecognize(client):
    while True:
        temp = input("Do you wanna turn on Face ID (type yes if you want): ")
        if temp == 'yes':
            RunFace(client)

USERNAME = 'HeoRey'
KEY = 'aio_tAaq928HAvklDgPLg640fMlta7Um'

feed_id_list = ['door','led','fan','led-changer','air-conditioner']

client = Adafruit_API(USERNAME, KEY, feed_id_list)
client.connect()
voiceThread = Thread(target = StartVoiceRecognition,args = [client])
voiceThread.daemon = True
voiceThread.start()
faceThread = Thread(target = EventFaceRecognize,args = [client])
faceThread.daemon = True
faceThread.start()

counter = 10

while(True):
    client.read_serial()
    time.sleep(1)