import pandas as pd 
import yaml
import json
import numpy as np
import fnmatch
import os
import re
import shutil
import glob
from PIL import Image

target_base_path = "/home/labuser/repos/DenseFusion/datasets/tommaso/tommaso_preprocessed/"
linemodPath = "LINEMOD/"

#Read relevant data from csv regarding boxes
boxList = pd.read_csv("annotations.csv",delimiter=";")
boxList.head()
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
total_folder = glob.glob("LINEMOD/*_ok/")
view_list = {i:name for i, name in enumerate(total_folder,1)}

objlist = {1:"siemens"}



# camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
#                     'ppx': intr.ppx, 'ppy': intr.ppy,
#                     'height': intr.height, 'width': intr.width,
#                     'depth_scale':profile.get_device().first_depth_sensor().get_depth_scale()
# }

#Pose estimation 
for n in objlist:
    #Create the yaml file as nested dictionary
    gt = {}
    info = {}
    train_final = []
    test_final = []
    path = target_base_path + "data/0{curr}/".format(curr = n)
    if not os.path.exists(path):
        os.mkdir(path)
    rgb = path + "rgb/"
    if not os.path.exists(rgb):
        os.mkdir(rgb)
    rgb = path + "mask/"
    if not os.path.exists(rgb):
        os.mkdir(rgb)
    rgb = path + "depth/"
    if not os.path.exists(rgb):
        os.mkdir(rgb)

    for l in view_list:
        no_Obj = []
        #Obj_tool_fold = linemodPath + objlist[n]
        #Go through all transoformations file 
        transform_dir =  view_list[l] + "transforms/" 
        for file in sorted(os.listdir(transform_dir)):
            #In case the are multiple object, each pose goes into a list 
            li = []

            curr = np.load(transform_dir + file)
            retrieve  = file[:-4]

            #convert the list to numeric values
            columns = Obj_boxList_group.get_group(view_list[l][:-1]).reset_index(drop=True)
            new_index = columns["Filename"].str.extract(r"\/([0-9]+)")[0]
            new_index = pd.to_numeric(new_index, errors='coerce')
            columns = columns.set_index(new_index)
            try: 
                tmp = pd.to_numeric(columns.loc[int(retrieve),boxCoordinates])
            except:
                print("No object in picture: " + str(file[:-4]))
                no_Obj.append(file[:-4])
                continue
            # if np.asarray(Image.open(view_list[l] + "depth/" + file[:-4] + ".png")).max() > 20000:
            #     idx =  str(l) + file[:-4]
            #     print("Invalid depth in picture: " + idx)
            #     no_Obj.append(file[:-4])
            #     continue

            idx =  str(l) + file[:-4]
            values = tmp.tolist()
            data = dict({"cam_R_m2c":curr[:3,:3].tolist(), "cam_t_m2c": curr[:3,3].tolist(), "obj_bb": values, "obj_id": 1})
            li.append(data)
            gt[int(idx)] = li
            info[int(idx)] = cam

            #Copy the depth, mask and rgb folders in the right location
            try:
                shutil.copy(view_list[l] + "JPEGImages/" + file[:-4] + ".jpg",  path + "rgb/" + idx + ".jpg" )
                shutil.copy(view_list[l] + "mask/" + file[:-4] + ".png",  path + "mask/" + idx + ".png" )
                shutil.copy(view_list[l] + "depth/" + file[:-4] + ".png",  path + "depth/" + idx + ".png" )
                # shutil.copytree(objlist[n] + "JPEGImages",path + "rgb")
                # shutil.copytree(objlist[n] + "mask",path + "mask")
                # shutil.copytree(objlist[n] + "depth",path + "depth")
            except Exception as e: 
                print("Something went wrong with file {}".format(objlist[n]))
                print(e)
        

        #Open the train and test files and extract valuable information. Save it in the proper format.
        n_date = re.compile(r"\/([0-9]+)")
        with open(view_list[l] + "train.txt") as train:
            train = train.read()
            train_instances = re.findall(n_date,train)
            train_final.extend([str(l) + curr for curr in train_instances if curr not in no_Obj])
            
        with open(view_list[l] + "test.txt") as test:
            test = test.read()
            test_instances = re.findall(n_date,test)
            test_final.extend([str(l) + curr for curr in test_instances if curr not in no_Obj])
        
        print("Processed: " + view_list[l])


    with open(path + "train.txt", "w+") as traintxt:
        for num in train_final:
            traintxt.write("{}\n".format(num))
    

    with open(path + "test.txt", "w+") as traintxt:
        for num in test_final:
            traintxt.write("{}\n".format(num))


    #Save json file
    with open(path + "gt.json", "w") as outfile:
        json.dump(gt,outfile)
    
    with open(path + "info.json", "w") as infofile:
        json.dump(info,infofile)

