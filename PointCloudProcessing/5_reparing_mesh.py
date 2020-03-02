import open3d as o3d
import trimesh 
pcd = o3d.io.read_point_cloud("mesh/mesh_siemens4.ply")
mesh = trimesh.load("mesh/mesh_siemens4.ply")
trimesh.repair.fill_holes(mesh)
mesh.export('mesh/mesh_siemens4_fixed.ply')
