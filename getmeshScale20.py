import numpy as np
import trimesh
import glob
import os
import yaml

def distance(point_one, point_two):
    return ((point_one[0] - point_two[0]) ** 2 +
            (point_one[1] - point_two[1]) ** 2 + (point_one[2] - point_two[2]) ** 2) ** 0.5

def max_distance(points):
    return max(distance(p1, p2) for p1, p2 in zip(points, points[1:]))

folders = glob.glob("LINEMOD/*/")

models_info = {}
for classlabel,folder in enumerate(folders):
    
    try:
        print(folder)

        mesh = trimesh.load(folder + folder[8:-1] +".ply")
        vertices = mesh.vertices
        maxD = max_distance(vertices.tolist())
        transposed = list(zip(*(vertices.tolist())))
        x_cords = transposed[0]*1000
        y_cords = transposed[1]
        z_cords = transposed[2]
        #The values are in m
        x_max = max(x_cords)-min(x_cords)
        y_max = max(y_cords)-min(y_cords)
        z_max = max(z_cords)-min(z_cords)
        print("Max vertice distance is: %f m." % maxD)
        print("max x: {}, max y: {} max z: {}".format(x_max, y_max,z_max))
        model = {"diameter": maxD, "min_x": min(x_cords), "min_y":min(y_cords), "min_z":min(z_cords), "size_x": max(x_cords),\
                "size_y":max(y_cords), "size_z":max(z_cords)}
    except:
        print("Mesh does not exist")
    
    models_info[classlabel+1] = model

    with open("models_info.yml","w") as outputfile:
        yaml.dump(models_info,outputfile)

    

