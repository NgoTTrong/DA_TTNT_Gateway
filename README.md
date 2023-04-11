# DA_TTNT_Gateway

First of all: create account adafruit then create some feed with these feed_id : fan, led, led-changer, door, air-conditioner, face-recognizer, humidity-sensor, light-sensor, temperature-sensor

1: Clone this project to your device

2: Starting gateway

  + replace username and key in file gateway.py by your adafruit username and key.
  + type in terminal: python gateway.py
 
3: Starting face recognizer:
  + replace username and key in file facerecognizer.py by your adafruit username and key.
  + type in terminal: python facerecognizer.py
  
 3: Starting voice:
  + replace username and key in file voice.py by your adafruit username and key.
  + type in terminal: python voice.py
  
  #About model AI
  
  You can add a new person for model to training
  
  by type in your teminal:
    + "python FaceCapturing.py" then according to instruction
    + "python train.py" to start training model
