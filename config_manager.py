import yaml
import os
import inspect
from typing import Optional, Tuple, Dict, Any

from logger import Logger

class ConfigFileManager:
    _instance: Optional['ConfigFileManager'] = None

    def __new__(cls, *args, **kwargs) -> 'ConfigFileManager':
        if not cls._instance:
            cls._instance = super(ConfigFileManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if not self.initialized:
            self.log_config: str = 'config/log.yaml'    # 로그 파일 경로
            self.img_config: str = 'config/image.yaml'  # 설정 파일 경로
            self.logger: Logger = Logger(self.get_log_path(), __class__.__name__)
            self.initialized = True
        
    def init_logger(self, msg: str) -> None:
        self.help_logger: Logger = Logger('log/log_yaml.log', __class__.__name__)
        self.help_logger.exception(msg)
    
    def get_log_path(self) -> Optional[str]:
        try:
            with open(self.log_config, 'r', encoding='UTF8') as file:
                config: Dict[str, Any] = yaml.safe_load(file)
            log_path = config['log_path']['total']
            if not os.path.exists(os.path.dirname(log_path)):
                raise FileNotFoundError(f'{log_path} doesn\'t exist.')
            else: #############로그 파일 여러개 등록 못한다????
                #self.init_logger(f'Successfully read log file from {log_path}')
                return log_path

        except FileNotFoundError as fnf:
            self.init_logger(f"[{inspect.currentframe().f_code.co_name}] Unavailable log file--> {fnf}")
        except KeyError as ke:
            self.init_logger(f"[{inspect.currentframe().f_code.co_name}] Using the wrong key--> {ke}")
        except Exception as e:
            self.init_logger(f"[{inspect.currentframe().f_code.co_name}] Check the error log--> {e}")
            
                    
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

            ######raise ValueError(f"{path['type']} need Check")

        except ValueError as ve:
            self.logger.exception(ve)
        except FileNotFoundError as fnf:
            self.logger.exception(f"[{inspect.currentframe().f_code.co_name}] Unavailable log file--> {fnf}")
        except KeyError as ke:
            self.logger.exception(f"[{inspect.currentframe().f_code.co_name}] Using the wrong key--> {ke}")
        except Exception as e:
            self.logger.exception(f"[{inspect.currentframe().f_code.co_name}] Check the error log--> {e}")

    def check_path(self, path: Optional[str]) -> bool:
        if path is None:
            self.logger.error("Path is Vacant, " + 
                             f"Called from: \"{inspect.currentframe().f_back.f_code.co_name}\"")
            return False
        
        elif not os.path.exists(os.path.dirname(path)):  ###### 새롭게 디렉토리 생성할건가?
            self.logger.error(f"Path is Wrong: {path}, " +
                              f"Called from: \"{inspect.currentframe().f_back.f_code.co_name}\"")
            return False
        
        else:
            self.logger.info(f"Correct Path: {path}" +
                             f"Called from: \"{inspect.currentframe().f_back.f_code.co_name}\"")
            return True
