import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import os

import sys
# examples/Python/Advanced/surface_reconstruction_poisson.py

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

pcd = o3d.io.read_point_cloud("cropped_3_experimental_True.ply")
#o3d.visualization.draw_geometries([pcd])
pcd = pcd.voxel_down_sample(voxel_size=0.001)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.00001, max_nn=5),fast_normal_computation=False)
print('run Poisson surface reconstruction')
#o3d.visualization.draw_geometries([pcd])
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=14, scale=1.5)
print(mesh)
o3d.visualization.draw_geometries([mesh])

print('visualize densities')
densities = np.asarray(densities)
density_colors = plt.get_cmap('plasma')(
    (densities - densities.min()) / (densities.max() - densities.min()))
density_colors = density_colors[:, :3]
density_mesh = o3d.geometry.TriangleMesh()
density_mesh.vertices = mesh.vertices
density_mesh.triangles = mesh.triangles
density_mesh.triangle_normals = mesh.triangle_normals
density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
o3d.visualization.draw_geometries([density_mesh])

print('remove low density vertices')
vertices_to_remove = densities < np.quantile(densities, 0.1)
mesh.remove_vertices_by_mask(vertices_to_remove)
print(mesh)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
o3d.io.write_triangle_mesh("mesh_result.ply", mesh)