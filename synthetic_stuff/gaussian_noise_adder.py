from PIL import Image
import cv2
import os
import numpy as np
import re
from multiprocessing import cpu_count, Pool

base_path = "LINEMOD/"
Synthetic_path  = base_path + "synthetic/"
synthetic_files = os.listdir(Synthetic_path)
a = re.compile(r".*img.*")
toConvert = list(filter(a.match, synthetic_files))
# for curr_file in toConvert:
#     img = cv2.imread(Synthetic_path+curr_file)
#     gaussian = np.round(np.random.normal(0, 5, (img.shape[0],img.shape[1],3)))
#     noisy_image = (img + gaussian)
#     noisy_image =  np.clip(noisy_image, 0, 255).astype(np.uint8)  
#     # apply guassian blur on src image
#     blurred_image = cv2.GaussianBlur(noisy_image,(3,3),cv2.BORDER_DEFAULT) 
#     cv2.imwrite(Synthetic_path+curr_file[:-4] + "blurred" + ".jpg",blurred_image)


multi = multiprocessing.Pool(num_workers)
result = multi.map(fun, toConvert)
multi.close()

def realistify(img):
    img = cv2.imread(Synthetic_path+curr_file)
    gaussian = np.round(np.random.normal(0, 5, (img.shape[0],img.shape[1],3)))
    noisy_image = (img + gaussian)
    noisy_image =  np.clip(noisy_image, 0, 255).astype(np.uint8)  
    # apply guassian blur on src image
    blurred_image = cv2.GaussianBlur(noisy_image,(3,3),cv2.BORDER_DEFAULT) 
    cv2.imwrite(Synthetic_path+curr_file[:-4] + "blurred" + ".jpg",blurred_image)