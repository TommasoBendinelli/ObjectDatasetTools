import pandas as pd 
import yaml
import numpy as np
import fnmatch
import os
import re
import shutil

target_base_path = "/home/labuser/repos/DenseFusion/datasets/tommaso/tommaso_preprocessed/"
linemodPath = "LINEMOD/"

#Read relevant data from csv regarding boxes
boxList = pd.read_csv("annotations.csv",delimiter=";")
boxCoordinates = boxList.columns[2:6]
print(boxList.head())
box = boxList.iloc[1]
print(box)

#Load Camera Intrinsics 
with open("camera_parameters.yml","r") as camera_file:
    camera_parameters = yaml.load(camera_file)

cam = {"cam_K": [camera_parameters['fx'], 0.0, camera_parameters['ppx'],\
        0.0, camera_parameters['fy'], camera_parameters['ppy'], \
        0.0, 0.0, 1.0], "depth_scale": camera_parameters['depth_scale']}

#Find all object folders
obj_dir = os.listdir(linemodPath)

#Read relevant data regarding transformation between picture and object 
local_directory =  linemodPath + "transforms/"

objlist = [1]



# camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
#                     'ppx': intr.ppx, 'ppy': intr.ppy,
#                     'height': intr.height, 'width': intr.width,
#                     'depth_scale':profile.get_device().first_depth_sensor().get_depth_scale()
# }

for n in objlist:
    path = target_base_path + "data/0{curr}/".format(curr = n)
    if not os.path.exists(path):
        os.mkdir(path)

    #Create the yaml file as nested dictionary
    gt = {}
    info = {}

    for file in sorted(os.listdir(local_directory)):
        #In case the are multiple object, each pose goes into a list 
        li = []

        curr = np.load(local_directory + file)
        idx = file[:-4]

        #convert the list to numeric values
        tmp = pd.to_numeric(boxList.loc[int(idx),boxCoordinates])
        values = tmp.tolist()
        data = dict({"cam_R_m2c":curr[:3,:3].tolist(), "cam_t_m2c": curr[:3,3].tolist(), "obj_bb": values, "obj_id": 1})
        li.append(data)
        gt[int(idx)] = li
        info[int(idx)] = cam
    

    #Open the train and test files and extract valuable information. Save it in the proper format.
    n_date = re.compile(r"\/([0-9]+)")
    with open(linemodPath + "train.txt") as n:
        n = n.read()
        results = re.findall(n_date,n)

    with open(path + "train.txt", "w+") as traintxt:
        for num in results:
            traintxt.write("{}\n".format(num))
    
    with open(linemodPath + "test.txt") as n:
        n = n.read()
        results = re.findall(n_date,n)

    with open(path + "test.txt", "w+") as traintxt:
        for num in results:
            traintxt.write("{}\n".format(num))

    #Copy the depth, mask and rgb folders in the right location
    try:
        shutil.copytree(linemodPath + "JPEGImages",path + "rgb")
        shutil.copytree(linemodPath + "mask",path + "mask")
        shutil.copytree(linemodPath + "depth",path + "depth")
    except: 
        pass 

    

    



    #Save yaml file
    with open(path + "gt.yml", "w") as outfile:
        yaml.dump(gt,outfile)
    
    with open(path + "info.yml", "w") as infofile:
        yaml.dump(info,infofile)