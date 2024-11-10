import unittest
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import os
from typing import Dict, Any, Tuple

from data_processing import DataProcessing

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.dp = DataProcessing()

    def test_remove_noise_statistical(self):
        # 테스트할 param 생성
        params = {'nb_neighbors': 20, 'std_ratio': 2.0}
        result = self.dp.remove_noise('data/test_data.pcd', 'statistical', params)

        # 테스트할 포인트 클라우드 생성
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
        o3d.io.write_point_cloud('data/test_data.pcd', point_cloud) # pcd or ply 사용 가능
        #o3d.io.write_point_cloud('data/test_data.ply', point_cloud) # pcd or ply 사용 가능
        
        # result가 PointCloud 인스턴스인지 확인
        self.assertIsInstance(result, o3d.geometry.PointCloud)
        self.assertGreater(len(np.asarray(result.points)), 0)

    def test_remove_noise_radius(self):
        # 테스트할 param 생성
        params = {'nb_points': 16, 'radius': 0.5}
        result = self.dp.remove_noise('data/test_data.pcd', 'radius', params)
        
        # 테스트할 포인트 클라우드 생성
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
        o3d.io.write_point_cloud('data/test_data.pcd', point_cloud) # pcd or ply 사용 가능

        # result가 PointCloud 인스턴스인지 확인
        self.assertIsInstance(result, o3d.geometry.PointCloud)
        self.assertGreater(len(np.asarray(result.points)), 0)

    def test_project_to_2d(self):
        # 테스트할 param 생성
        projection_vector = np.array([1, 0, 0])  # x축으로 투영
        
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
        
        projected_points = self.dp.project_to_2d(point_cloud, projection_vector)
        
        # 2D 형태 확인
        self.assertEqual(projected_points.shape[1], 2)  

    def test_create_depth_map(self):
        # 테스트할 param 생성
        projected_points = np.random.uniform(0.5, 1.0, size=(100, 2))
        depth_map_path = 'result/test_depth_map.png'
        image_size = (100, 100)

        self.dp.create_depth_map(projected_points, depth_map_path, image_size)

        # 이미지 파일이 저장되었는지 확인
        self.assertTrue(os.path.exists(depth_map_path), "Depth map image not saved.")

        # 이미지 확인
        depth_map_image = plt.imread(depth_map_path)
        self.assertEqual(depth_map_image.shape[:2], image_size)

    def test_create_heat_map(self):
        # 테스트할 param 생성
        projected_points = np.random.uniform(0.5, 1.0, size=(100, 2))
        heat_map_path = 'result/test_heat_map.png'
        image_size = (100, 100)
        
        self.dp.create_heat_map(projected_points, heat_map_path, image_size)
        
        # 이미지 파일이 저장되었는지 확인
        self.assertTrue(os.path.exists(heat_map_path), "Heat map image not saved.")
        
        # 이미지 확인
        heat_map_image = plt.imread(heat_map_path)
        self.assertEqual(heat_map_image.shape[:2], image_size)

if __name__ == '__main__':
    unittest.main()
