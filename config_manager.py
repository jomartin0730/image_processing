import yaml
import os
import inspect
from typing import Optional, Tuple, Dict, Any

from logger import Logger

class ConfigFileManager:
    def __init__(self) -> None:
        self.img_config: str = 'config/image.yaml'  # 설정 파일 경로
        self.log_path: str
        self.use_file: bool
        self.use_print: bool
        self.log_path, self.use_file, self.use_print = self.get_log_settings()
        self.logger: Logger = self.init_logger()      
            
    def init_logger(self) -> Logger:
        return Logger(self.log_path, self.use_file, self.use_print)
    
    def log_error(self, msg: str) -> None:
        self.help_logger: Logger = Logger('log/yaml_error.log', True, True)
        self.help_logger.exception(msg, f"[{self.__class__.__name__}] ")

    def get_log_settings(self) -> Optional[Tuple[str, bool, bool]]:
        try:
            with open(self.img_config, 'r', encoding='UTF8') as file:
                config: Dict[str, Any] = yaml.safe_load(file)
                
            log_path: str = config['log_settings']['path']
            use_file: bool = config['log_settings']['use_file']
            use_print: bool = config['log_settings']['use_print']

            if not isinstance(use_file, bool):
                raise ValueError("use_file must be a boolean value.")
            if not isinstance(use_print, bool):
                raise ValueError("use_print must be a boolean value.")
            
            if not os.path.exists(os.path.dirname(log_path)) or log_path is None:
                raise FileNotFoundError(f'{log_path} doesn\'t exist.')
            else:
                return log_path, use_file, use_print
        
        except ValueError as ve:
            self.log_error(f"{ve}")
        except FileNotFoundError as fnf:
            self.log_error(f"Unavailable file. Check the yaml file--> {fnf}")
        except KeyError as ke:
            self.log_error(f"Using the wrong yaml key. Check the yaml file--> {ke}")
        except Exception as e:
            self.log_error(f"Check the error log--> {e}")

        return None
              
    def get_img_path(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        try:
            with open(self.img_config, 'r', encoding='UTF8') as file:
                config: Dict[str, Any] = yaml.safe_load(file)

            for path in config['3Dfile_paths']:
                if path['type'] == 'pcd_file' and self.check_path(path['path']):
                    self.logger.info(f'Successfully read {path["type"]} from {path["path"]}')
                    return path['path'], config
                
                elif path['type'] == 'ply_file' and self.check_path(path['path']):
                    self.logger.info(f'Successfully read {path["type"]} from {path["path"]}')
                    return path['path'], config

            raise FileNotFoundError(f"Check the {path['type']} and {path['path']}")

        except ValueError as ve:
            self.logger.exception(ve)
        except FileNotFoundError as fnf:
            self.logger.exception(f"Unavailable image file. Check the yaml file--> {fnf}")
        except KeyError as ke:
            self.logger.exception(f"Using the wrong yaml key. Check the yaml file--> {ke}")
        except Exception as e:
            self.logger.exception(f"Check the error log--> {e}")

    def check_path(self, path: Optional[str]) -> bool:
        if path is None:
            self.logger.error(
                f"[{inspect.currentframe().f_back.f_code.co_name}] "
                f"Path is None", 
                f"[{self.__class__.__name__}] "
            )
            return False

        directory = os.path.dirname(path)
        
        # 디렉토리 존재 여부 확인 
        if not os.path.exists(directory): ##-> save image의 경우 이상함 수정 필요
            self.logger.error(
                f"[{inspect.currentframe().f_back.f_code.co_name}] "
                f"Directory does not exist: {directory}", 
                f"[{self.__class__.__name__}] "
            )
            return False

        # 파일 존재 여부 확인 --> depth_map과 분리 필요
        # if not os.path.isfile(path):
        #     self.logger.error(
        #         f"[{inspect.currentframe().f_back.f_code.co_name}] "
        #         f"File does not exist: {path}", 
        #         f"[{self.__class__.__name__}] "
        #     )
        #     return False

        # 모든 확인이 통과한 경우
        self.logger.info(
            f"Correct path: {path}", 
        )
        return True