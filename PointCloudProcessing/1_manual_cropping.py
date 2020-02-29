import open3d as o3d
import numpy as np
print("Manual geometry cropping")
print(
    "1) Press 'Y' twice to align geometry with negative direction of y-axis"
)
print("2) Press 'K' to lock screen and to switch to selection mode")
print("3) Drag for rectangle selection,")
print("   or use ctrl + left click for polygon selection")
print("4) Press 'C' to get a selected geometry and to save it")
print("5) Press 'F' to switch to freeview mode")
pcd = o3d.io.read_point_cloud("registeredScene.ply")
o3d.visualization.draw_geometries_with_editing([pcd])