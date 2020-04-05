import numpy as np
import os
from PIL import Image

PATH = "LINEMOD/siemens_kuka10_ok/mask/"
PATH_transform =  "LINEMOD/siemens_kuka10_ok/transforms/"
masks = os.listdir(PATH_transform)
np.load(PATH_transform + "0.npy")
print(np.load(PATH_transform + "0.npy"))
label = np.array(Image.open(PATH+"0.png"))

print(np.max(np.sum(label,axis=1)/255))
#pint(label(where=))
