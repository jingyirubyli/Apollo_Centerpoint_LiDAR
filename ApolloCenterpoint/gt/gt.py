import numpy as np
import open3d as o3d
import os
import time

def visualize_point_cloud_with_bounding_boxes(pcd_file_path, bounding_boxes=None):
    """
    Visualize a point cloud and draw bounding boxes at specified locations.
    
    Args:
        pcd_file_path (str): Path to the PCD file
        bounding_boxes (list): List of dictionaries with bounding box parameters
                              Each dict should contain 'center', 'size', 'rotation' (in radians)
    """
    # Load point cloud
    print(f"Loading point cloud from {pcd_file_path}")
    start_time = time.time()
    pcd = o3d.io.read_point_cloud(pcd_file_path)
    load_time = time.time() - start_time
    
    print(f"Point cloud loaded in {load_time:.2f} seconds")
    print(f"Point cloud has {len(pcd.points)} points")
    
    # Get point cloud information
    points = np.asarray(pcd.points)
    min_bound = np.min(points, axis=0)
    max_bound = np.max(points, axis=0)
    print(f"Point cloud bounds: Min {min_bound}, Max {max_bound}")
    
    # Optional: Downsample for performance if the point cloud is very large
    if len(pcd.points) > 1000000:
        print("Large point cloud detected. Downsampling for better visualization performance...")
        pcd = pcd.voxel_down_sample(voxel_size=0.1)
        print(f"Downsampled to {len(pcd.points)} points")

    # Create visualization objects
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Point Cloud with Bounding Boxes", width=1200, height=800)
    
    # Add geometry
    vis.add_geometry(pcd)

    # If no bounding boxes are provided, try to automatically segment and create boxes
    if bounding_boxes is None:
        print("No bounding boxes specified. Trying automatic clustering...")
        
        # For large point clouds, we might want to use DBSCAN clustering
        eps = (max_bound - min_bound).max() / 50  # A reasonable starting epsilon
        min_points = 50
        
        print(f"Running DBSCAN clustering with eps={eps:.2f}, min_points={min_points}")
        start_time = time.time()
        
        # Estimate normals if needed for better segmentation
        pcd.estimate_normals()
        
        # Perform clustering
        labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points))
        cluster_time = time.time() - start_time
        print(f"Clustering completed in {cluster_time:.2f} seconds")
        
        max_label = labels.max()
        print(f"Point cloud has {max_label + 1} clusters")
        
        # Create a bounding box for each cluster
        bounding_boxes = []
        for i in range(max_label + 1):
            # Get points for this cluster
            cluster_points = points[labels == i]
            
            if len(cluster_points) < 50:  # Skip small clusters
                continue
                
            # Create oriented bounding box for this cluster
            cluster_pcd = o3d.geometry.PointCloud()
            cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)
            obb = cluster_pcd.get_oriented_bounding_box()
            
            # Add to our list
            bounding_boxes.append({
                'center': obb.center,
                'size': obb.extent,
                'rotation': obb.R  # This is a 3x3 rotation matrix
            })
            
            print(f"Cluster {i}: {len(cluster_points)} points, Center: {obb.center}, Size: {obb.extent}")
    
    # Add specified bounding boxes
    for i, box_params in enumerate(bounding_boxes):
        center = box_params['center']
        size = box_params['size']
        
        # Handle different rotation formats
        if 'rotation' in box_params:
            rotation = box_params['rotation']
            if rotation.shape == (3,):
                # Euler angles
                R = o3d.geometry.get_rotation_matrix_from_xyz(rotation)
            elif rotation.shape == (3, 3):
                # Rotation matrix
                R = rotation
            else:
                R = np.identity(3)
        else:
            R = np.identity(3)
        
        # Create an oriented bounding box
        box = o3d.geometry.OrientedBoundingBox(center, R, size)
        
        # Set color (优先使用用户指定的颜色)
        if 'color' in box_params:
            box.color = np.array(box_params['color'])
        else:
            # 默认颜色循环
            colors = [[1,0,0], [0,1,0], [0,0,1]]
            box.color = np.array(colors[i % len(colors)])
        
        # Add to visualizer
        vis.add_geometry(box)
    
    # Configure the visualizer
    opt = vis.get_render_option()
    opt.background_color = np.array([1, 1, 1])  # background
    opt.point_size = 1.0
    
    # Set view control
    vc = vis.get_view_control()
    vc.set_zoom(0.7)
    
    # Run the visualizer
    print("Visualizing point cloud with bounding boxes...")
    vis.run()
    vis.destroy_window()

def main():
    # Specify the path to your complete PCD file
    pcd_file_path = "/Users/jingyili/Desktop/fusion/denoised-frames/denoised_frame_250.pcd"  # Replace with your actual file path
    
    # Define specific bounding boxes if needed
    # Example bounding boxes (you should replace with your specific locations)
    bounding_boxes = [
        # {
        #     'center': np.array([12200, 3000, -800]),
        #     'size': np.array([500, 400, 600]),
        #     'rotation': np.array([0, 0, 0]),
        #     'color': [0, 1, 0] # Green
        # },
        {
            'center': np.array([25800, 1700, 750]),
            'size': np.array([600, 600, 1800]),
            'rotation': np.array([0, 0, 0]),
            'color': [1, 0, 0]  # Red 
        },
        {
            'center': np.array([26000, -2300, 650]),
            'size': np.array([600, 600, 1800]),
            'rotation': np.array([0, 0, 0]),
            'color': [1, 0, 0]  # Red 
        }
    ]
    
    # Visualize with specified bounding boxes
    visualize_point_cloud_with_bounding_boxes(pcd_file_path, bounding_boxes )
    
    # Alternatively, to use automatic bounding box detection:
    # visualize_point_cloud_with_bounding_boxes(pcd_file_path)

if __name__ == "__main__":
    main()
    