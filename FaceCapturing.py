import cv2
import os

IMG_PATH = 'data'
count = 50
userName = input("Input user name: ")
USR_PATH = os.path.join(IMG_PATH, userName)
leap = 1
if not(os.path.isdir(USR_PATH)):
    os.mkdir(USR_PATH)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
while cap.isOpened() and count:
    isSuccess, frame = cap.read()
    if leap%2:
        path = str(USR_PATH+'/{}.jpg'.format(str(50 - count)))
        cv2.imwrite(path,frame)
        count-=1
    leap+=1
    cv2.imshow('Face Capturing', frame)
    if cv2.waitKey(1)&0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()