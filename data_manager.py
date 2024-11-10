import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

from config_manager import ConfigFileManager

class DataManager:
    def __init__(self) -> None:
        self.cm: ConfigFileManager = ConfigFileManager()

    def get_depths(self, projected_points: np.ndarray) -> Tuple[float, float]:
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

        check: bool = self.cm.check_path(path, False)
        if check:
            plt.imsave(path, image, cmap=cmap) # 이미지 저장
            self.cm.logger.info(f"{map_type.capitalize()} map saved at {path}")
        else:
            self.cm.logger.error(f"{map_type.capitalize()} map can't saved") # 경로가 지정되지 않은 경우 저장하지 않음
