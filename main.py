import numpy as np
from typing import Optional, Any

from data_processing import DataProcessing
#from config_manager import ConfigFileManager
from logger import Logger


def main(args: Optional[Any] = None) -> None:
    dp: DataProcessing = DataProcessing()
    #cm: ConfigFileManager = ConfigFileManager()
    logger: Logger = Logger(dp.dm.cm.get_log_path(), __name__)

    img_3d_path, config_file = dp.dm.cm.get_img_path()
    # try:

    # 노이즈 제거
    img_3d: Any = dp.remove_noise(
        img_3d_path, 
        algorithm=config_file['algorithm_settings']['noise_removal']['algorithms'], 
        params=config_file['algorithm_settings']['noise_removal']['params']
    )

    # 2D 투영
    projected_points: np.ndarray = dp.project_to_2d(
        img_3d, 
        projection_vector=np.array(config_file['algorithm_settings']['projection_vector'])
    )

    # 2D Depth map 생성
    dp.create_depth_map(
        projected_points, 
        depth_map_path=config_file['2Dfile_paths']['depth_map']
    )

    # 2D Heat map 생성
    dp.create_heat_map(
        projected_points, 
        heat_map_path=config_file['2Dfile_paths']['heat_map']
    )
    # except ValueError as ve:
    #     logger.exception(f"Value Error: {ve}")
    # except FileNotFoundError as fe:
    #     logger.exception(f"File Error: {fe}")
    # except Exception as e:
    #     logger.exception(f"Unknown Error: {e}")
    # except KeyboardInterrupt:
    #     sys.exit(1)

if __name__ == '__main__':
    main()
