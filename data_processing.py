import numpy as np
import open3d as o3d
from typing import Dict, Any, Tuple

from data_manager import DataManager

class DataProcessing:
    def __init__(self) -> None:
        self.dm: DataManager = DataManager()

    def remove_noise(self, 
                     path: str, 
                     algorithm: str, 
                     params: Dict[str, Any]
        ) -> o3d.geometry.PointCloud:
        
        pcd: o3d.geometry.PointCloud = o3d.io.read_point_cloud(path)
        cl: o3d.geometry.PointCloud
        ind: np.ndarray
        
        if algorithm == 'statistical':
            cl, ind = pcd.remove_statistical_outlier(
                nb_neighbors=params['nb_neighbors'], 
                std_ratio=params['std_ratio']
            )
            self.dm.cm.logger.info(f'Number of points after noise removal: {len(np.asarray(cl.points))}')
            return cl
        
        elif algorithm == 'radius':
            cl, ind = pcd.remove_radius_outlier(
                nb_points=params['nb_points'], 
                radius=params['radius']
            )
            processed_img: o3d.geometry.PointCloud = pcd.select_by_index(ind)
            self.dm.cm.logger.info(f'Number of points after noise removal: {len(np.asarray(processed_img.points))}')
            return processed_img
        
        else:
            self.dm.cm.logger.error('Check removal algorithm')
            raise KeyError("Unknown noise removal algorithm")
 
    def project_to_2d(self, 
                      pcd: o3d.geometry.PointCloud, 
                      projection_vector: np.ndarray
        ) -> np.ndarray:
        
        points: np.ndarray = np.asarray(pcd.points)
        projected_points: np.ndarray = points @ projection_vector.reshape(-1, 1)  # 벡터 형태로 변환
        
        if projected_points.size % 2 != 0:
            projected_points = projected_points[:-1]  # 마지막 포인트 제거

        projected_points = projected_points.reshape(-1, 2)  # 2D 배열로 변환

        if projected_points.size == 0:
            self.dm.cm.logger.warning(f'Projected points size is not even. Current size: {projected_points}')
        else:
            self.dm.cm.logger.info(f'Number of projected points: {projected_points.size}')
            
        return projected_points
    
    def create_depth_map(self, projected_points: np.ndarray, depth_map_path: str, image_size: Tuple[int, int] = (100, 100)) -> None:
        depth_map_image: np.ndarray = np.zeros(image_size, dtype=np.float32)  # Depth map 초기화
        count_map: np.ndarray = np.zeros(image_size, dtype=int)  # 카운트 배열 초기화

        max_depth, min_depth = self.dm.get_depths(projected_points)

        for point in projected_points:
            x: int = int((point[0] - min_depth) / (max_depth - min_depth) * (image_size[1] - 1))  # X 좌표
            y: int = int((point[1] - min_depth) / (max_depth - min_depth) * (image_size[0] - 1))  # Y 좌표

            if 0 <= x < image_size[1] and 0 <= y < image_size[0]:
                depth_map_image[y, x] += point[0]  # depth 값을 해당 위치에 저장
                count_map[y, x] += 1  # 카운트 증가

        # 평균화
        depth_map_image[count_map > 0] /= count_map[count_map > 0]

        self.dm.cm.logger.info(f'Depth map parameters: {depth_map_image.size}, {depth_map_path}')
        self.dm.save_image(depth_map_image, depth_map_path, map_type="depth", cmap='gray')  # depth map image 저장

    def create_heat_map(self, 
                        projected_points: np.ndarray, 
                        heat_map_path: str, 
                        image_size: Tuple[int, int] = (100, 100)
        ) -> None:
        
        heat_map_image: np.ndarray = np.zeros((image_size[0], image_size[1], 3), dtype=np.uint8)  # 3채널 RGB 이미지 초기화
        max_depth, min_depth = self.dm.get_depths(projected_points)
        
        for point in projected_points:
            # X와 Y 좌표를 계산합니다.
            x: int = int((point[0] - min_depth) / (max_depth - min_depth) * (image_size[1] - 1))
            y: int = int((point[1] - min_depth) / (max_depth - min_depth) * (image_size[0] - 1))

            if 0 <= x < image_size[1] and 0 <= y < image_size[0]:
                heat_map_image[y, x] = [255, 0, 0]  # Red color for heat

        self.dm.cm.logger.info(f'Heat map parameters: {heat_map_image.size}, {heat_map_path}')
        self.dm.save_image(heat_map_image, heat_map_path, map_type="heat")  # heat map image 저장
