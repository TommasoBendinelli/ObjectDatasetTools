	

# examples/Python/Advanced/interactive_visualization.py

import numpy as np
import copy
import open3d as o3d
import sys
import os

def demo_crop_geometry():
    print("Demo for manual geometry cropping")
    print(
        "1) Press 'Y' twice to align geometry with negative direction of y-axis"
    )
    print("2) Press 'K' to lock screen and to switch to selection mode")
    print("3) Drag for rectangle selection,")
    print("   or use ctrl + left click for polygon selection")
    print("4) Press 'C' to get a selected geometry and to save it")
    print("5) Press 'F' to switch to freeview mode")
    pcd = o3d.io.read_point_cloud("../../TestData/ICP/cloud_bin_0.pcd")
    o3d.visualization.draw_geometries_with_editing([pcd])


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def pick_points(pcd):
    print("")
    print(
        "1) Please pick at least three correspondences using [shift + left click]"
    )
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    return vis.get_picked_points()


def demo_manual_registration():
    print("Demo for manual ICP")

    cad_mesh = o3d.io.read_triangle_mesh("cad_models/siemens.ply")
    cad_mesh = cad_mesh.scale(1/1000)
    cad = cad_mesh.sample_points_poisson_disk(50000)
    


    #source = o3d.io.read_triangle_mesh("scaledSiemens.ply")
    #source = source.sample_points_poisson_disk(2000)
    #print("point_cloud/cropped/" + sys.argv[1] + "_cropped1.ply")
    if sys.argv[2] == "1":
        pcd = o3d.io.read_point_cloud("point_cloud/cropped/" + sys.argv[1] +  ".ply")
    else:
        pcd = o3d.io.read_point_cloud("point_cloud/augmented/backup"+sys.argv[1]+"best.ply")
    pcd = pcd.voxel_down_sample(voxel_size = 0.0005)

    t = -cad.points[0]+pcd.points[5]
    cad.translate(t)
    o3d.visualization.draw_geometries([cad,pcd])
    # cad.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    #     radius=0.00001, max_nn=5),fast_normal_computation=False)
    # pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    #     radius=0.00001, max_nn=5),fast_normal_computation=False)

    print("Visualization of two point clouds before manual alignment")
    #draw_registration_result(source, target, np.identity(4))
    while True:
        source = copy.deepcopy(cad)
        target = copy.deepcopy(pcd)
        cad_res = copy.deepcopy(cad_mesh)
        # pick points from two point clouds and builds correspondences
        picked_id_target = pick_points(target)
        picked_id_source = pick_points(source)
        assert (len(picked_id_source) >= 3 and len(picked_id_target) >= 3)
        assert (len(picked_id_source) == len(picked_id_target))
        corr = np.zeros((len(picked_id_source), 2))
        corr[:, 0] = picked_id_source
        corr[:, 1] = picked_id_target

        # estimate rough transformation using correspondences
        print("Compute a rough transform using the correspondences given by user")
        p2p = o3d.registration.TransformationEstimationPointToPoint()
        trans_init = p2p.compute_transformation(source, target,
                                                o3d.utility.Vector2iVector(corr))

        source.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
             radius=0.00001, max_nn=5),fast_normal_computation=False)
        target.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
             radius=0.00001, max_nn=5),fast_normal_computation=False)
        # point-to-point ICP for refinement
        print("Perform point-to-point ICP refinement")
        threshold = 0.001  # 3cm distance threshold
        reg_p2p = o3d.registration.registration_icp(
            source, target, threshold, trans_init,
            o3d.registration.TransformationEstimationPointToPoint())
        cad_res.translate(t)
        cad_res.transform(reg_p2p.transformation)
        # rot = reg_p2p.transformation[:3,:3]
        # trasl = reg_p2p.transformation[:3,3]
        # cad_mesh.translate(-trasl)
        o3d.visualization.draw_geometries([cad_res, target])
        print("")
        print("Do you like the result?")
        like = input('Please type Y or N')  
        if like == "Y":
            o3d.io.write_triangle_mesh("mesh/" + sys.argv[1] + ".ply", cad_res)
            
            break


if __name__ == "__main__":
    #demo_crop_geometry()
    demo_manual_registration()
