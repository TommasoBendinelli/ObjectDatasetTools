import numpy as np
import cv2
import glob
from copy import deepcopy
from random import randint
import csv
from PIL import Image
import os
import re
import json

base_path = "SYN/"
child = sys.argv[1]
base_dataset_folder = os.path.join(base_path,child)
a = re.compile(r".*topcam.json")
total_list = utils.return_process_files(base_dataset_folder = base_dataset_folder, regular_expression=a)

for files in tqdm(total_list):
    curr_json = json.open(files)
    for obj in curr_json["objects"]:
        get_class(obj)

    im = Image.open(files)
    rgb_im = im.convert('RGB')
    rgb_im.save(files[:-3] + "jpg")
    #os.remove(curr_folder + curr_file)

def get_class():


def get_id():


def get_bounding_box ():

base_path = "LINEMOD/"
Synthetic_path  = base_path + "synthetic/"
synthetic_files = os.listdir(Synthetic_path)
a = re.compile(r".*layer.*")
b = re.compile(r".*id.*")
layer_pics = list(filter(a.match, synthetic_files))
id_pics = list(filter(b.match, synthetic_files))

for layer_pic in layer_pics:
    idx = layer_pic[:][6:11]
    id_pic = [id_pic for id_pic in id_pics if idx in id_pic][0]
    layer_pic_path = os.path.join(Synthetic_path,layer_pic)
    layer_pic = cv2.imread(layer_pic_path,0)
    id_pic_path = os.path.join(Synthetic_path,id_pic)
    id_pic = cv2.imread(id_pic_path)
    id_pic[layer_pic == 255] = 0
    #cv2.imshow(id_pic_path,id_pic)
    #cv2.waitKey(0)
    #unique, occurence =  np.unique(layer_pic, return_counts = True)
    unique, occurence =  np.unique(id_pic.reshape(-1, id_pic.shape[2]),axis=0, return_counts = True)
    for idx, obj in enumerate(unique):
        if not np.any(obj):
            continue
        curr_pic = id_pic.copy()
        if occurence[idx] > 500:
            curr_pic[curr_pic != obj] = 0
            gray = cv2.cvtColor(curr_pic, cv2.COLOR_BGR2GRAY)
            _, contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                cnt = max(contours, key=cv2.contourArea)
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(id_pic,(x,y),(x+w,y+h),255,1)
            # data.append(str(x))
            # data.append(str(y))
            # data.append(str(x+w))
            # data.append(str(y+h))
            # data.append(str(0))
            # allinfo.append(data)
            cv2.imshow("window",id_pic)
            cv2.waitKey(0)
    #total_objs = np.unique(id_pic)
    

for curr_file in toConvert:
    im = Image.open(Synthetic_path + curr_file)
    rgb_im = im.convert('RGB')
    rgb_im.save(Synthetic_path + curr_file[:-3] + "jpg")
    os.remove(Synthetic_path + curr_file)

allinfo = []
allinfo.append(["Filename","Annotation tag","Upper left corner X","Upper left corner Y","Lower right corner X","Lower right corner Y","Occluded"])
writer = csv.writer(open("annotations.csv", "w"), delimiter=";")
folders = "LINEMOD/synthetic/"
for folder in folders:
    classlabel = 0
    len_dataset = len(glob.glob1(folder+"JPEGImages","*.jpg"))
    for id in range(len_dataset):
        try:
            data = []
            imagepath = folder+"JPEGImages/" + str(id) + ".jpg"
            data.append(imagepath)
            data.append(classlabel)
            img_original = cv2.imread(imagepath)
            mask_dir = folder + "mask/" + str(id) + ".png"
            mask = cv2.imread(mask_dir,0)
            thresh = cv2.threshold(mask.copy(), 30, 255, cv2.THRESH_BINARY)[1]

            _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnt = max(contours, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img_original,(x,y),(x+w,y+h),(0,255,0),2)
            data.append(str(x))
            data.append(str(y))
            data.append(str(x+w))
            data.append(str(y+h))
            data.append(str(0))
            allinfo.append(data)
        
            cv2.imshow("window",img_original)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass

writer.writerows(allinfo)
