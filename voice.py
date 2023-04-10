import speech_recognition as sr
import pyttsx3
from adafruit_api import Adafruit_API

r = sr.Recognizer()
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init() 
    engine.say(command)
    engine.runAndWait()

def run(client):
    with sr.Microphone() as source2:
        print('Say something\n<----->')
        r.adjust_for_ambient_noise(source2, duration=0.2)
        print('Ready to record\n<----->')
        SpeakText("I'm here. Please command to me!")
        audio2 = r.listen(source2)
        print('Audio captured\n<----->')
        try:
            MyText = r.recognize_google(audio2, language="vi-VN")
            MyText = MyText.lower()
            print("Did you say ",MyText)
            if ("bật" in MyText and "đèn" in MyText):
                SpeakText("Okey turn on the light")
                client.publish('led','1')
            elif ("tắt" in MyText and "đèn" in MyText):
                SpeakText("Okey turn off the light")
                client.publish('led','0')
            elif ("mở" in MyText and "cửa" in MyText):
                SpeakText("Okey open the door")
                client.publish('door','1')
            elif ("đóng" in MyText and "cửa" in MyText):
                SpeakText("Okey close the door")
                client.publish('door','0')
            elif ("mở" in MyText and "máy" in MyText and "lạnh" in MyText):
                SpeakText("Okey turn on the air conditioner")
                client.publish('air-conditioner','100')
            elif ("tắt" in MyText and "máy" in MyText and "lạnh" in MyText):
                SpeakText("Okey turn off the air conditioner")
                client.publish('air-conditioner','0')

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Plz try agains")
def start_signal_detect(client):
    with sr.Microphone() as source2:
        print('Say something\n<----->')
        r.adjust_for_ambient_noise(source2, duration=0.2)
        print('Ready to record\n<----->')
        audio2 = r.listen(source2)
        print('Audio captured\n<----->')
        try:
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            if ("hey google" in MyText):
                run(client)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Plz try agains")

USERNAME = 'HeoRey'
KEY = 'aio_ddPb315ep1qBs6wwAk1TOSEahLq2'

if __name__ == "__main__":
    client = Adafruit_API(USERNAME, KEY, [])
    client.connect()
    while True:
        start_signal_detect(client)