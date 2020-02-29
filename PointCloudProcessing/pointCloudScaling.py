import open3d as o3d
import o3d.geometry.sample_points_disk 

mesh = o3d.io.read_triangle_mesh("LINEMOD/siemens2_backup/70384708.ply")
mesh = mesh.scale(1/1000)
o3d.io.write_triangle_mesh("LINEMOD/siemens2_backup/scaledSiemens.ply", mesh)