import trimesh
import open3d as o3d
import numpy as np


def ply_vtx(path):
    f = open(path)
    assert f.readline().strip() == "ply"
    f.readline()
    f.readline()
    N = int(f.readline().split()[-1])
    while f.readline().strip() != "end_header":
        continue
    pts = []
    for _ in range(N):
        pts.append(np.float32(f.readline().split()[:3]))
    return np.array(pts)

pt  = ply_vtx('mesh/obj_01_linemod.ply')
print("Number of points: {}".format(len(pt)))
pl = o3d.geometry.PointCloud()
pl.points = o3d.utility.Vector3dVector(pt)
o3d.visualization.draw_geometries([pl])
#o3d.io.write_point_cloud("point_cloud/siemens4_segmented.ply".format(experimental), res)

pt = o3d.io.read_triangle_mesh('mesh/mesh_siemens4.ply')
pt = pt.sample_points_uniformly(5841)
o3d.visualization.draw_geometries([pt])

pt = o3d.io.read_point_cloud('point_cloud/siemens4_segmented.ply')
pt = pt.voxel_down_sample(voxel_size = 0.002)
o3d.visualization.draw_geometries([pt])

