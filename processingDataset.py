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
Obj_boxList_group = boxList.groupby("Annotation tag")
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

#Find all object folders and return the absolute path
# obj_dirs = os.listdir(linemodPath)
# obj_dirs = [linemodPath + obj_dir + "/" for obj_dir in obj_dirs ]


#Read relevant data regarding transformation between picture and object 
#local_directory =  linemodPath + "transforms/"
objlist = {1: "test3/", 2:"siemens4/", 3:"siemens5/"}



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

    Obj_tool_fold = linemodPath + objlist[n]
    #Go through all transoformations file 
    transform_dir =  Obj_tool_fold + "transforms/" 
    for file in sorted(os.listdir(transform_dir)):
        #In case the are multiple object, each pose goes into a list 
        li = []

        curr = np.load(transform_dir + file)
        idx = file[:-4]

        #convert the list to numeric values
        columns = Obj_boxList_group.get_group(Obj_tool_fold[:-1]).reset_index(drop=True)
        tmp = pd.to_numeric(columns.loc[int(idx),boxCoordinates])
        values = tmp.tolist()
        data = dict({"cam_R_m2c":curr[:3,:3].tolist(), "cam_t_m2c": curr[:3,3].tolist(), "obj_bb": values, "obj_id": 1})
        li.append(data)
        gt[int(idx)] = li
        info[int(idx)] = cam
    

    #Open the train and test files and extract valuable information. Save it in the proper format.
    n_date = re.compile(r"\/([0-9]+)")
    with open(Obj_tool_fold + "train.txt") as n:
        n = n.read()
        results = re.findall(n_date,n)

    with open(path + "train.txt", "w+") as traintxt:
        for num in results:
            traintxt.write("{}\n".format(num))
    
    with open(Obj_tool_fold + "test.txt") as n:
        n = n.read()
        results = re.findall(n_date,n)

    with open(path + "test.txt", "w+") as traintxt:
        for num in results:
            traintxt.write("{}\n".format(num))

    #Copy the depth, mask and rgb folders in the right location
    try:
        shutil.copytree(Obj_tool_fold + "JPEGImages",path + "rgb")
        shutil.copytree(Obj_tool_fold + "mask",path + "mask")
        shutil.copytree(Obj_tool_fold + "depth",path + "depth")
        print("Files copied: ".format(Obj_tool_fold))
    except Exception as e: 
        print("Something went wrong with file {}".format(Obj_tool_fold))
        print(e)

    

    



    #Save yaml file
    with open(path + "gt.yml", "w") as outfile:
        yaml.dump(gt,outfile)
    
    with open(path + "info.yml", "w") as infofile:
        yaml.dump(info,infofile)