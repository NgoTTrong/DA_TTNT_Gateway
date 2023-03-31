from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import cv2
import os

mtcnn = MTCNN(margin=0, keep_all=True, min_face_size=40) 
resnet = InceptionResnetV1(pretrained='vggface2').eval() 

load_data = torch.load('data.pt') 
embedding_list = load_data[0] 
name_list = load_data[1] 

flag = False
def RunFace(client):
    global flag
    cam = cv2.VideoCapture(0) 
    while True:
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
                        if name == "masked":
                            frame = cv2.putText(frame,'Please take off the mask', (int(box[0]) - 100,int(box[1]) - 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 1, cv2.LINE_8)
                        else:
                            frame = cv2.putText(frame, name + '_{:.2f}'.format(min_dist), (int(box[0]) - 100,int(box[1]) - 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 2, cv2.LINE_8)
                            flag = True
                            client.publish('door','1')
                            break
                    else:
                        frame = cv2.putText(frame, "Unknow", (int(box[0]),int(box[1])), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2, cv2.LINE_8)
                        frame = cv2.rectangle(frame, (int(box[0]),int(box[1])) , (int(box[2]),int(box[3])), (0, 0, 255), 2)

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