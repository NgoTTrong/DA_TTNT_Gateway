from adafruit_api import Adafruit_API
import time
from threading import Thread
from voice import *

USERNAME = 'HeoRey'
KEY = 'aio_ddPb315ep1qBs6wwAk1TOSEahLq2'

feed_id_list = ['door','led','fan','led-changer','air-conditioner']

client = Adafruit_API(USERNAME, KEY, feed_id_list)
client.connect()


while(True):
    client.read_serial()
    time.sleep(1)