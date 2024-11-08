import numpy as np
import open3d as o3d
from typing import Optional, Any

from data_processing import DataProcessing


def main(args: Optional[Any] = None) -> None:
    try:
        dp: DataProcessing = DataProcessing()

        # load image path, yaml file
        img_3d_path, config_file = dp.dm.cm.get_img_path()

        # remov noise
        img_3d: o3d.geometry.PointCloud = dp.remove_noise(
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
    
    except TypeError as te:
        dp.dm.cm.logger.exception(
            f"Type has the error. Check the type--> {te}", 
            f"[{__name__}] "
        )
    except KeyError as ke:
        dp.dm.cm.logger.exception(
            f"Key has the error. Check the yaml file--> {ke}", 
            f"[{__name__}] "
        )
    except Exception as e:
        dp.dm.cm.logger.exception(
            f"Check the error log--> {e}", 
            f"[{__name__}] "
        )

if __name__ == '__main__':
    main()
