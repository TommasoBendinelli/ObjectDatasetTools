import open3d as o3d
import numpy as np
pcd = o3d.io.read_point_cloud("registeredScene.ply")
#o3d.visualization.draw_geometries_with_editing([pcd])
plane_model, inliers = pcd.segment_plane(0.01,3,250)
[a, b, c, d] = plane_model
print(f"Plane model: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

if c > 0.01:
    x0 = np.array([0, 0, -d/c])
else:
    x0 = np.array([0, -d/b, 0])

inlier_cloud = pcd.select_down_sample(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])

outlier_cloud = pcd.select_down_sample(inliers, invert=True)

o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

#Put here the pointcloud
pcd = o3d.io.read_point_cloud("cropped_1.ply")

#Find the projection into the plane
obj = np.asarray(pcd.points)
n = np.array([a,b,c])
scalars = np.reshape(np.dot((obj - x0),n),(-1,1))

#Experimental, discard all points that comprise the old plane and above 0.0001.
#In this way noise point right above the ground are not reprojected.
experimental = True
if experimental:
    boolcond = np.reshape(scalars < -0.003 ,-1)
    curr = obj[boolcond]
    curr_scalar = scalars[boolcond]
    proj = curr - np.multiply(n,curr_scalar)
    #Find all the points below the plane and discard them and then add proj
    boolcond = np.reshape(scalars < -0.003 ,-1)
    obj = obj[boolcond]
    points = np.concatenate((obj,proj))
    

else:
    proj = obj - np.multiply(n,scalars)
    boolcond = np.reshape(scalars < 0 ,-1)
    obj = obj[boolcond]
    points = np.concatenate((obj,proj))





#Experimental, discard all points that comprise the old plane and above 0.01.
# boolcond = np.reshape(scalars < 0,-1)
# obj = obj[boolcond]
# points = np.concatenate((obj,proj))


#Create point cloud object and visualize it 
pl = o3d.geometry.PointCloud()
pl.points = o3d.utility.Vector3dVector(points)

print("If the result is not what expected try to change the sign in boolcond")
o3d.visualization.draw_geometries([pl])
o3d.io.write_point_cloud("cropped_3_experimental_{}.ply".format(experimental), pl)


#o3d.visualization.draw_geometries([pl])

#Poisson algorithm


#Save it 


# inlier_cloud = pcd.select_down_sample(inliers)
# inlier_cloud.paint_uniform_color([1.0, 0, 0])

# outlier_cloud = pcd.select_down_sample(inliers, invert=True)

# o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

