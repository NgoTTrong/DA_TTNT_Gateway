from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import cv2
import os
from voice import SpeakText
from adafruit_api import Adafruit_API

def EventFaceRecognize(client):
    while True:
        temp = input("Do you wanna turn on Face ID (type yes if you want): ")
        if temp == 'yes':
            result = RunFace(client)
            print(result)
            if result == "UnKnow":
                SpeakText("Pip pip pip pip ...")
                client.publish("door",'0')
                client.publish('face-recognizer',"A stranger person is standing in front of the house")
            elif result == "masked":
                SpeakText("Please take out the mask")
                client.publish('face-recognizer',"A person with mask is standing in front of the house")
            elif result == None:
                continue
            else:
                SpeakText("Open the door")
                client.publish("door",'1')
                client.publish('face-recognizer',str(result) + " open the door")

def RunFace(client):
    flag = False
    cam = cv2.VideoCapture(0)
    result = None
    counter = 20
    while True:
        if counter == 0:
            break
        counter-=1
        isSuccess, frame = cam.read()
        if not isSuccess:
            print("fail to grab frame, try again")
            break
            
        img = Image.fromarray(frame)
        img_cropped_list, prob_list = mtcnn(img, return_prob=True) 
        if img_cropped_list is not None:
            boxes, _ = mtcnn.detect(img)
                    
            for i, prob in enumerate(prob_list):
                if prob>0.90:
                    emb = resnet(img_cropped_list[i].unsqueeze(0)).detach() 
                    
                    dist_list = []
                    
                    for idx, emb_db in enumerate(embedding_list):
                        dist = torch.dist(emb, emb_db).item()
                        dist_list.append(dist)

                    min_dist = min(dist_list) # get minumum dist value
                    min_dist_idx = dist_list.index(min_dist) # get minumum dist index
                    name = name_list[min_dist_idx] # get name corrosponding to minimum dist
                    
                    box = boxes[i]                 
                    if min_dist<0.90:
                        frame = cv2.rectangle(frame, (int(box[0]),int(box[1])) , (int(box[2]),int(box[3])), (0,255,0), 2)
                        frame = cv2.putText(frame, name + '_{:.2f}'.format(min_dist), (int(box[0]) - 100,int(box[1]) - 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 2, cv2.LINE_8)
                        result = name
                    else:
                        frame = cv2.putText(frame, "Unknow", (int(box[0]),int(box[1])), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2, cv2.LINE_8)
                        frame = cv2.rectangle(frame, (int(box[0]),int(box[1])) , (int(box[2]),int(box[3])), (0, 0, 255), 2)
                        result = "UnKnow"
        cv2.imshow("Face Recognition", frame)
            
        if flag == True:
            flag = False
            print('Opening the door...')
            break
        k = cv2.waitKey(1)
        if k%256==27: # ESC
            print('Esc pressed, closing...')
            break
    cam.release()
    cv2.destroyAllWindows()
    return result


USERNAME = 'HeoRey'
KEY = 'aio_TEjN17FO7meqFOqQTrykGm00oAoh'

if __name__ == "__main__":
    mtcnn = MTCNN(margin=0, keep_all=True, min_face_size=40) 
    resnet = InceptionResnetV1(pretrained='vggface2').eval() 

    load_data = torch.load('data.pt') 
    embedding_list = load_data[0] 
    name_list = load_data[1] 

    client = Adafruit_API(USERNAME, KEY, [])
    client.connect()
    EventFaceRecognize(client)