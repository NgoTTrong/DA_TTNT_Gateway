from adafruit_api import Adafruit_API
import time
from threading import Thread
from voice import *

USERNAME = 'HeoRey'
KEY = 'aio_TEjN17FO7meqFOqQTrykGm00oAoh'

feed_id_list = ['door','led','fan','led-changer','air-conditioner']

client = Adafruit_API(USERNAME, KEY, feed_id_list,"COM4")
client.connect()


while(True):
    client.read_serial()
    time.sleep(1)