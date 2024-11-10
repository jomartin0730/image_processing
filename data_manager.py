import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

from config_manager import ConfigFileManager

class DataManager:
    def __init__(self) -> None:
        self.cm: ConfigFileManager = ConfigFileManager()

    def get_depths(self, projected_points: np.ndarray) -> Tuple[float, float]:
        """X와 Y 좌표를 계산을 위한 최대 최소 depth 값을 획득한다.
        
        Args:
            projected_points : 2D 배열로 변환된 투영된 포인트.
        Returns:
            float 형태의 최대 최소 depth 값.
            
        """
        max_depth: float = np.max(projected_points[:, 0])  # x 좌표에서 최대 깊이
        min_depth: float = np.min(projected_points[:, 0])  # x 좌표에서 최소 깊이
        self.cm.logger.info(f"Calculated to max depth {max_depth}, min depth {min_depth}")
        return max_depth, min_depth
    
    def save_image(
            self, 
            image: np.ndarray, 
            path: str, 
            map_type: str, 
            cmap: Optional[str] = None
        ) -> None:
        """이미지를 저장하는 메소드. 이미지 저장 경로가 지정되지 않은 경우에는 이미지를 저장하지 않는다.
        따라서 이미지 저장 전에 경로가 empty 여부, 디렉토리 존재 여부를 확인한다.
        디렉토리가 비어있는 경우에는 디렉토리를 생성한다.
        
        Args:
            image    : 이미지 프로세싱이 완료된 depth map 또는 heat map 2D 이미지 파일.
            path     : YAML 설정 파일에서 지정된 경로.
            map_type : 로그 기록을 위한 depth map, heat map을 구분하는 문자열.
            cmap     : depth map인 경우 gray로 고정.
        Returns:
            없음.
            
        """
        if not self.cm.empty_path(path) and self.cm.directory_exist(path, True):
            plt.imsave(path, image, cmap=cmap) # 이미지 저장
            self.cm.logger.info(f"{map_type.capitalize()} map saved at {path}")
        else:
            self.cm.logger.error(f"{map_type.capitalize()} map can't saved") # 경로가 지정되지 않은 경우 저장하지 않음
