from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import os
import glob
mtcnn = MTCNN(margin=0, keep_all=False, min_face_size=40)
resnet = InceptionResnetV1(pretrained='vggface2').eval() 
PATH = 'data'

name_list = []
embedding_list = [] 

for user in os.listdir(PATH):
    embeds = []
    for file in glob.glob(os.path.join(PATH, user)+'/*.jpg'):
        try:
            img = Image.open(file)
        except:
            continue
        face, prob = mtcnn(img, return_prob=True) 
        if face is not None and prob>0.9:
            emb = resnet(face.unsqueeze(0)) 
            embeds.append(emb.detach()) 
    if len(embeds) == 0:
        continue
    embedding = torch.cat(embeds).mean(0, keepdim=True) #calculate mean of user's embedding matrix
    embedding_list.append(embedding)
    name_list.append(user)
  
# save data
data = [embedding_list, name_list] 
torch.save(data, 'data.pt') # saving data.pt file