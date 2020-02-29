import open3d as o3d
import trimesh 
pcd = o3d.io.read_point_cloud("saved_result.ply")
mesh = trimesh.load("saved_result.ply")
trimesh.repair.fill_holes(mesh)
mesh.export('fixed.ply')
