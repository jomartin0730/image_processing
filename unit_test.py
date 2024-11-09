import unittest
import numpy as np
import open3d as o3d
from data_processing import DataProcessing  # 해당 클래스가 정의된 파일의 이름
from unittest.mock import MagicMock
from typing import Dict, Any, Tuple

class TestDataProcessing(unittest.TestCase):
    
    def setUp(self):
        self.dp = DataProcessing()
        self.dp.dm = MagicMock()  # DataManager의 mock 객체 생성

    def test_remove_noise_statistical(self):
        params = {'nb_neighbors': 20, 'std_ratio': 2.0}
        result = self.dp.remove_noise('data/sample_data.pcd', 'statistical', params)

        self.assertIsInstance(result, o3d.geometry.PointCloud)
        self.assertGreater(len(np.asarray(result.points)), 0)

    # def test_remove_noise_radius(self):
    #     # 테스트할 포인트 클라우드 생성
    #     pcd = o3d.geometry.PointCloud()
    #     pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
    #     o3d.io.write_point_cloud('data/sample_data.pcd', pcd)

    #     params = {'nb_points': 10, 'radius': 0.1}
    #     result = self.dp.remove_noise('data/sample_data.pcd', 'radius', params)

    #     self.assertIsInstance(result, o3d.geometry.PointCloud)
    #     self.assertGreater(len(np.asarray(result.points)), 0)

    def test_project_to_2d(self):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
        projection_vector = np.array([1, 0, 0])  # x축으로 투영
        projected_points = self.dp.project_to_2d(pcd, projection_vector)

        self.assertEqual(projected_points.shape[1], 2)  # 2D 형태 확인

    def test_create_depth_map(self):
        projected_points = np.random.rand(50, 2) * 100  # 랜덤 2D 포인트 생성
        self.dp.dm.get_depths = MagicMock(return_value=(100, 0))  # Mock으로 깊이 값 반환
        self.dp.create_depth_map(projected_points, 'data/depth_map.png', (100, 100))

        # depth_map_image가 생성되었는지 확인
        self.dp.dm.save_image.assert_called_once()

    def test_create_heat_map(self):
        projected_points = np.random.rand(50, 2) * 100  # 랜덤 2D 포인트 생성
        self.dp.dm.get_depths = MagicMock(return_value=(100, 0))  # Mock으로 깊이 값 반환
        self.dp.create_heat_map(projected_points, 'data/heat_map.png', (100, 100))

        # heat_map_image가 생성되었는지 확인
        self.dp.dm.save_image.assert_called_once()

if __name__ == '__main__':
    unittest.main()
