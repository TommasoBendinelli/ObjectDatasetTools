import open3d as o3d 

#Put here the pointcloud
pcd = o3d.io.read_point_cloud("point_cloud/siemens4_segmented.ply")

cad = o3d.io.read_triangle_mesh("cad_models/siemens.ply")
cad = cad.scale(1/1000)
cad = cad.sample_points_uniformly(10000)


cad.translate(-cad.points[0]+pcd.points[5])
o3d.visualization.draw_geometries([cad,pcd])
