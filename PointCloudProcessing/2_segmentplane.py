import open3d as o3d
import numpy as np
pcd = o3d.io.read_point_cloud("registeredScene.ply")
#o3d.visualization.draw_geometries_with_editing([pcd])
plane_model, inliers = pcd.segment_plane(0.01,3,250)
[a, b, c, d] = plane_model
print(f"Plane model: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
pcd = o3d.io.read_point_cloud("registeredScene_cropped2.ply")
if c > 0.01:
    x0 = np.array([0, 0, -d/c])
else:
    x0 = np.array([0, -d/b, 0])



#Find the projection into the plane
obj = np.asarray(pcd.points)
n = np.array([a,b,c])
scalars = np.reshape(np.dot((obj - x0),n),(-1,1))
proj = obj - np.multiply(n,scalars)

#Find all the points below the plane and discard them and then add proj
boolcond = np.reshape(scalars < 0 ,-1)
obj = obj[boolcond]
points = np.concatenate((obj,proj))


#Create final point cloud object and visualize it 
pl = o3d.geometry.PointCloud()
pl.points = o3d.utility.Vector3dVector(points)
o3d.io.write_point_cloud("closed_point_cloud.ply", pl)
print("Point cloud saved")

#o3d.visualization.draw_geometries([pl])

#Poisson algorithm


#Save it 


# inlier_cloud = pcd.select_down_sample(inliers)
# inlier_cloud.paint_uniform_color([1.0, 0, 0])

# outlier_cloud = pcd.select_down_sample(inliers, invert=True)

# o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

