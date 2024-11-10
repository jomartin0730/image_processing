import numpy as np
import open3d as o3d
from typing import Dict, Any, Tuple

from data_manager import DataManager

class DataProcessing:
    def __init__(self) -> None:
        self.dm: DataManager = DataManager()

    def remove_noise(
            self, 
            path: str, 
            algorithm: str, 
            params: Dict[str, Any]
        ) -> o3d.geometry.PointCloud:
        """PCD 또는 PLY 파일의 노이즈를 제거한다.
        
        이 함수는 'statistical', 'radius' 2가지의 open3d의 outlier removal 알고리즘 사용이 가능하다.
        
        Args:
            path      : YAML 설정 파일에 지정한 PCD 또는 PLY 파일 위치.
            algorithm : YAML 설정 파일에 지정한 알고리즘. 주석 처리를 통해 선택하여 사용 가능하다.
            params    : 'statistical'의 경우 'nb_neighbors'와 'std_ratio', 'radius'의 경우 'nb_points'와 'radius'
                        모든 파라미터들은 YAML 파일에 딕셔너리 형태로 지정되어 있다.
        Returns:
            노이즈가 제거된 포인트 클라우드.
        Raises:
            ValueError: 'statistical', 'radius' 이외의 값이 전달된 경우.
            
        """
        pcd: o3d.geometry.PointCloud = o3d.io.read_point_cloud(path)
        cl: o3d.geometry.PointCloud
        ind: np.ndarray
        
        if algorithm == 'statistical':
            cl, ind = pcd.remove_statistical_outlier(
                nb_neighbors=params['nb_neighbors'],
                std_ratio=params['std_ratio']
            )
            self.dm.cm.logger.info(f'Number of points after statistical noise removal: {len(np.asarray(cl.points))}')
            return cl
        
        elif algorithm == 'radius':
            cl, ind = pcd.remove_radius_outlier(
                nb_points=params['nb_points'], 
                radius=params['radius']
            )
            processed_img: o3d.geometry.PointCloud = pcd.select_by_index(ind)
            self.dm.cm.logger.info(f'Number of points after radius noise removal: {len(np.asarray(processed_img.points))}')
            return processed_img
        
        else:
            self.dm.cm.logger.error('Check removal algorithm')
            raise ValueError("Unknown noise removal algorithm")

    def project_to_2d(
            self, 
            pcd: o3d.geometry.PointCloud, 
            projection_vector: np.ndarray
        ) -> np.ndarray:
        """3D 이미지를 벡터 방향에 따라 투영 후 2D 배열로 변환한다.
        
        투영된 이미지의 개수가 홀수개인 경우 마지막 포인트 제거한다.
        projected_points의 개수가 0인 경우는 warning 로그를 출력 및 기록한다.
        
        Args:
            pcd               : 노이즈 제거가 완료된 포인트 클라우드.
            projection_vector : 투영 벡터 방향을 설정하는 파라미터. YAML 파일에서 수정 가능하다. 
                                현재는 X 방향으로 설정되어 있다.
        Returns:
            2D 배열로 변환된 투영된 포인트.
            
        """
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
    
    def create_depth_map(
            self, 
            projected_points: np.ndarray, 
            depth_map_path: str, 
            image_size: Tuple[int, int] = (100, 100)
        ) -> None:
        """투영된 포인트들을 2D depth map으로 생성한다.
        
        최대 최소 depth 값을 가져와 투영된 포인트들과 계산하여, 2차원 좌표값을 획득한다. 이후 depth 값을 해당 위치에 저장한다.
        평균화 작업을 진행하고, 이미지 저장을 위해 파라미터 값을 DataManager 클래스의 save_image 메소드에 넘겨준다.
        float32 타입이며, 사진 색상은 회색이다.
        
        Args:
            projected_points : 2D 배열로 변환된 투영된 포인트.
            depth_map_path   : 이미지 저장을 위한 경로. YAML 설정 파일에 해당 경로가 지정되어 있다. 
            image_size       : 적당한 이미지 크기.
        Returns:
            없음.
            
        """
        depth_map_image: np.ndarray = np.zeros(image_size, dtype=np.float32)  # Depth map 초기화
        count_map: np.ndarray = np.zeros(image_size, dtype=int)  # 카운트 배열 초기화

        max_depth, min_depth = self.dm.get_depths(projected_points)

        for point in projected_points:
            x: int = int((point[0] - min_depth) / (max_depth - min_depth) * (image_size[1] - 1))
            y: int = int((point[1] - min_depth) / (max_depth - min_depth) * (image_size[0] - 1))

            if 0 <= x < image_size[1] and 0 <= y < image_size[0]:
                depth_map_image[y, x] += point[0]  # depth 값을 해당 위치에 저장
                count_map[y, x] += 1  # 카운트 증가

        # 평균화
        depth_map_image[count_map > 0] /= count_map[count_map > 0]

        self.dm.cm.logger.info(f'Depth map parameters: {depth_map_image.size}, {depth_map_path}')
        self.dm.save_image(depth_map_image, depth_map_path, map_type="depth", cmap='gray')  # depth map image 저장


    def create_heat_map(
            self, 
            projected_points: np.ndarray, 
            heat_map_path: str, 
            image_size: Tuple[int, int] = (100, 100)
        ) -> None:
        """투영된 포인트들을 2D heat map으로 생성.
        
        최대 최소 depth 값을 가져와 투영된 포인트들과 계산하여, 2차원 좌표값을 획득한다. 
        이후 heat_map_image 배열에 x, y 좌표값을 대입한다.
        이미지 저장을 위해 파라미터 값을 DataManager 클래스의 save_image 메소드에 넘겨준다.
        uint8 타입이며, 사진 색상은 붉은색으로 지정했다.
        
        Args:
            projected_points : 2D 배열로 변환된 투영된 포인트.
            heat_map_path    : 이미지 저장을 위한 경로. YAML 설정 파일에 해당 경로가 지정되어 있다. 
            image_size       : 적당한 이미지 크기.
        Returns:
            없음.
            
        """        
        heat_map_image: np.ndarray = np.zeros((image_size[0], image_size[1], 3), dtype=np.uint8)  # 3채널 RGB 이미지 초기화
        max_depth, min_depth = self.dm.get_depths(projected_points)
        
        for point in projected_points:
            x: int = int((point[0] - min_depth) / (max_depth - min_depth) * (image_size[1] - 1))
            y: int = int((point[1] - min_depth) / (max_depth - min_depth) * (image_size[0] - 1))

            if 0 <= x < image_size[1] and 0 <= y < image_size[0]:
                heat_map_image[y, x] = [255, 0, 0]  # 붉은색으로 표시

        self.dm.cm.logger.info(f'Heat map parameters: {heat_map_image.size}, {heat_map_path}')
        self.dm.save_image(heat_map_image, heat_map_path, map_type="heat")  # heat map image 저장
