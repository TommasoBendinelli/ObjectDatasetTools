	

# examples/Python/Advanced/interactive_visualization.py

import numpy as np
import copy
import open3d as o3d
import sys


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

    first_cloud = o3d.io.read_point_cloud("point_cloud/augmented/best.ply")
    pcd = o3d.io.read_point_cloud("point_cloud/cropped/" + sys.argv[1] + "_cropped1.ply")
    # pcd = pcd.voxel_down_sample(voxel_size = 0.002)

    # t = -first_cloud.points[0]+pcd.points[5]
    # first_cloud.translate(t)
    o3d.visualization.draw_geometries([first_cloud,pcd])
    first_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.00001, max_nn=5),fast_normal_computation=False)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.00001, max_nn=5),fast_normal_computation=False)
    source = first_cloud
    target = pcd
    #print("Visualization of two point clouds before manual alignment")
    #draw_registration_result(source, target, np.identity(4))
    while True:
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

        # point-to-point ICP for refinement
        print("Perform point-to-point ICP refinement")
        threshold = 0.001  # 3cm distance threshold
        reg_p2p = o3d.registration.registration_icp(
            source, target, threshold, trans_init,
            o3d.registration.TransformationEstimationPointToPoint())
        # first_cloud.translate(t)
        first_cloud.transform(reg_p2p.transformation)
        # rot = reg_p2p.transformation[:3,:3]
        # trasl = reg_p2p.transformation[:3,3]
        # cad_mesh.translate(-trasl)
        o3d.visualization.draw_geometries([first_cloud, target])
        #draw_registration_result(source, target, reg_p2p.transformation)
        print("")
        print("Do you like the result o you want to do it again?")
        like = input('Please type Y or N')   
        if like == "Y":
            res = first_cloud + target
            o3d.io.write_point_cloud("point_cloud/augmented/best.ply", res)
            o3d.io.write_point_cloud("point_cloud/augmented/backup"+sys.argv[1]+"best.ply", res)
            break




if __name__ == "__main__":
    demo_manual_registration()
