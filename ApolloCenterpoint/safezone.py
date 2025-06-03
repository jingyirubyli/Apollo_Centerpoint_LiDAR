import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from shapely.geometry import Point, Polygon

def compute_polar_angle(reference, point):
    """
    计算点 `point` 相对于 `reference` 的极角
    """
    x0, y0 = reference
    x, y = point
    return np.arctan2(y - y0, x - x0)

def sort_points_by_polar_angle(points):
    """
    选择参考点并按极角排序点集
    """
    points = np.array(points) 
    reference = min(points, key=lambda p: (p[1], p[0])) 
    sorted_points = sorted(points, key=lambda p: compute_polar_angle(reference, p)) 
    return reference, np.array(sorted_points)

def is_worker_inside_safe_zone(worker_pos, safe_zone_points):
    """
    判断工人是否在安全区域内
    """
    polygon = Polygon(safe_zone_points) 
    worker_point = Point(worker_pos)
    return polygon.contains(worker_point) or polygon.touches(worker_point) 

def plot_safe_zone_and_workers(cone_positions, worker_positions):
    """
    计算并可视化基于 cones 形成的安全区域，并检测工人是否在安全区域内
    """
    plt.figure(figsize=(8, 6))

    if len(cone_positions) > 4:
        hull = ConvexHull(cone_positions)
        convex_hull_points = cone_positions[hull.vertices]
    else:
        convex_hull_points = cone_positions

    reference, sorted_hull_points = sort_points_by_polar_angle(convex_hull_points)

    plt.scatter(cone_positions[:, 0], cone_positions[:, 1], color='red', label="Cones", s=100)
    plt.scatter(reference[0], reference[1], color='blue', label="Reference Point", s=100)

    sorted_hull_points = np.vstack([sorted_hull_points, sorted_hull_points[0]])  # 形成闭合多边形
    plt.fill(sorted_hull_points[:, 0], sorted_hull_points[:, 1], 'lightblue', alpha=0.5, label="Safe Zone")

    for i in range(len(sorted_hull_points) - 1):
        x1, y1 = sorted_hull_points[i]
        x2, y2 = sorted_hull_points[i + 1]
        plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)

    for i, worker_pos in enumerate(worker_positions):
        inside = is_worker_inside_safe_zone(worker_pos, sorted_hull_points)
        color = 'green' if inside else 'black'
        status = "Safe" if inside else "Danger!"
        
        plt.scatter(worker_pos[0], worker_pos[1], color=color, label=f"Worker {i+1}: {status}", s=100)
        plt.text(worker_pos[0] + 0.2, worker_pos[1] + 0.2, f"W{i+1}", fontsize=12, color=color, weight='bold')

    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Traffic Cone Defined Safe Zone & Worker Detection")
    plt.grid(True)
    plt.show()

# 注意计算位置代表点(底面中心)

# 自定义cone
cone_positions = np.array([
    [1, 1], [5, 2], [3, 5], [7, 3]
])

# 自定义worker
worker_positions = np.array([
    [4, 3], 
    [8, 3]   # 在安全区外
])

plot_safe_zone_and_workers(cone_positions, worker_positions)