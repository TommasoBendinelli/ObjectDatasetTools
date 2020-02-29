# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details

# examples/Python/Advanced/surface_reconstruction_ball_pivoting.py

import open3d as o3d
import numpy as np
import os
import matplotlib.pyplot as plt

# def problem_generator():
#     o3d.utility.set_verbosity_level(o3d.utility.Debug)

#     points = []
#     normals = []
#     for _ in range(4):
#         for _ in range(4):
#             pt = (np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0)
#             points.append(pt)
#             normals.append((0, 0, 1))
#     points = np.array(points, dtype=np.float64)
#     normals = np.array(normals, dtype=np.float64)
#     pcd = o3d.io.read_point_cloud("closed_point_cloud.ply")
#     pcd.points = o3d.utility.Vector3dVector(points)
#     pcd.normals = o3d.utility.Vector3dVector(normals)
#     radii = [1, 2]
#     yield pcd, radii

#     o3d.utility.set_verbosity_level(o3d.utility.Info)

#     gt_mesh = o3d.geometry.TriangleMesh.create_sphere()
#     gt_mesh.compute_vertex_normals()
#     pcd = gt_mesh.sample_points_poisson_disk(100)
#     radii = [0.5, 1, 2]
#     yield pcd, radii

#     gt_mesh = meshes.bunny()
#     gt_mesh.compute_vertex_normals()
#     pcd = gt_mesh.sample_points_poisson_disk(2000)
#     radii = [0.005, 0.01, 0.02, 0.04]
#     yield pcd, radii

#     gt_mesh = meshes.armadillo()
#     gt_mesh.compute_vertex_normals()
#     pcd = gt_mesh.sample_points_poisson_disk(2000)
#     radii = [5, 10]
#     yield pcd, radii


# if __name__ == "__main__":
#     for pcd, radii in problem_generator():

import time 
radii = [1,2]
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Info)

pcd = o3d.io.read_point_cloud("closed_point_cloud.ply")
pcd = pcd.voxel_down_sample(voxel_size=0.002)
#cd = pcd.sample_points_poisson_disk(10000)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.1, max_nn=30))
o3d.visualization.draw_geometries([pcd])
start = time.time()
rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
   pcd, o3d.utility.DoubleVector(radii))
# alpha = np.log10(0.5)
# mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
#rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd,0.5)

# print('run Poisson surface reconstruction')
# mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
#     pcd, depth=8)
# print(mesh)
# print('visualize densities')
# densities = np.asarray(densities)
# density_colors = plt.get_cmap('plasma')(
#     (densities - densities.min()) / (densities.max() - densities.min()))
# density_colors = density_colors[:, :3]
# density_mesh = o3d.geometry.TriangleMesh()
# density_mesh.vertices = mesh.vertices
# density_mesh.triangles = mesh.triangles
# density_mesh.triangle_normals = mesh.triangle_normals
# density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
# o3d.visualization.draw_geometries([density_mesh])

# print('remove low density vertices')
# vertices_to_remove = densities < np.quantile(densities, 0.1)
# mesh.remove_vertices_by_mask(vertices_to_remove)
# print(mesh)
# o3d.visualization.draw_geometries([mesh])
print(time.time()-start)
o3d.visualization.draw_geometries([pcd, rec_mesh])

# o3d.visualization.draw_geometries([pcd, rec_mesh])