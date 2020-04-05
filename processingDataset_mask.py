import pandas as pd 
import yaml
import numpy as np
import fnmatch
import os
import re
import shutil
import json
import glob

ObjectDataTools_path = "/home/labuser/repos/ObjectDatasetTools/"
#instance_base_path = "/home/labuser/repos/ObjectDatasetTools/dataset/tommaso/"
linemodPath = "LINEMOD/"

path = "/home/labuser/repos/tensorflow-models/datasets/tommaso/"

#Read relevant data from csv regarding boxes
boxList = pd.read_csv(ObjectDataTools_path+ "annotations.csv",delimiter=";")
Obj_boxList_group = boxList.groupby("Annotation tag")
boxCoordinates = boxList.columns[2:6]
box = boxList.iloc[1]

#Load Camera Intrinsics 
with open(ObjectDataTools_path + "camera_parameters.yml","r") as camera_file:
    camera_parameters = yaml.load(camera_file)

cam = {"cam_K": [camera_parameters['fx'], 0.0, camera_parameters['ppx'],\
        0.0, camera_parameters['fy'], camera_parameters['ppy'], \
        0.0, 0.0, 1.0], "depth_scale": camera_parameters['depth_scale'],\
        "height": camera_parameters['height'], "width": camera_parameters['width'] }

#Read relevant data regarding transformation between picture and object 
#local_directory =  linemodPath + "transforms/"
total_folder = glob.glob("LINEMOD/*_ok/")
view_list = {i:name for i, name in enumerate(total_folder,1)}
print("Directories to process")
print(view_list)

objlist = {1:"siemens"}

# camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
#                     'ppx': intr.ppx, 'ppy': intr.ppy,
#                     'height': intr.height, 'width': intr.width,
#                     'depth_scale':profile.get_device().first_depth_sensor().get_depth_scale()
# }
box = []
#Pose estimation 
for n in objlist:
    no_Obj =[]
    rgb = path + "rgb/"
    if not os.path.exists(rgb):
        os.mkdir(rgb)
    rgb = path + "mask/"
    if not os.path.exists(rgb):
        os.mkdir(rgb)

    for l in view_list:
        print("Processing: " + view_list[l])
        #Obj_tool_fold = linemodPath + objlist[n]
        #Go through all transoformations file 
        transform_dir =  view_list[l] + "transforms/" 
        for file in sorted(os.listdir(transform_dir)):
            #In case the are multiple object, each pose goes into a list 
            curr = np.load(transform_dir + file)
            idx = file[:-4]

            #convert the list to numeric values
            columns = Obj_boxList_group.get_group(view_list[l][:-1]).reset_index(drop=True)
            new_index = columns["Filename"].str.extract(r"\/([0-9]+)")[0]
            new_index = pd.to_numeric(new_index, errors='coerce')
            columns = columns.set_index(new_index)
            try: 
                tmp = pd.to_numeric(columns.loc[int(idx),boxCoordinates])
            except:
                print(idx)
                print("No object in picture: " + str(file[:-4]))
                no_Obj.append(file[:-4])
                continue
            values = tmp.tolist()
            new_idx = str(l) + str(idx)
            data = dict({"idx": int(str(l) + str(idx)), "obj_bb": values, "obj_id": n, "image_height": cam['height'], "image_width": cam['width']})
            box.append(data)
            try:
                shutil.copy(ObjectDataTools_path + view_list[l] + "JPEGImages/" + idx + ".jpg",  path + "rgb/" + str(new_idx) + ".jpg" )
                shutil.copy(ObjectDataTools_path + view_list[l] + "mask/" + idx + ".png",  path + "mask/" + str(new_idx) + ".png" )
            except Exception as E:
                print("This exception")
                print(E)


#Save yaml file
with open(path + "info.json", "w") as outfile:
    json.dump(box,outfile)

# with open(path + "camera_intrinsic.json", "w") as infofile:
#     json.dump(info,infofile)

