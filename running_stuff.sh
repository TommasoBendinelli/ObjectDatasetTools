#Collecting Data
python3 record2.py "LINEMOD/$1"
python3 compute_gt_poses.py "LINEMOD/$1"
python3 register_scene.py "LINEMOD/$1"
cp LINEMOD/$1/registeredScene.ply PointCloudProcessing/point_cloud/original/$1_original.ply

#Processing Data
cd PointCloudProcessing/
echo $PWD
source env/bin/activate
python3 1_manual_cropping.py $1
#python3 3_point_cloud_ICP.py $1
python3 interactivePointCloud.py $1 "1"
deactivate 
cd .. 
cp PointCloudProcessing/mesh/$1.ply LINEMOD/$1/mesh_result.ply
python3 create_label_files.py "LINEMOD/$1"
python3 inspectMasks.py "LINEMOD/$1_ok"