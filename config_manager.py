import yaml
import os
import inspect
from typing import Optional, Tuple, Dict, Any

from logger import Logger

class ConfigFileManager:
    def __init__(self) -> None:
        self.img_config: str = 'config/image.yaml'  # 설정 파일 경로
        self.yaml_log: str = 'log/yaml_error.log'  # YAML 에러용 로그 경로
        self.log_path: str
        self.use_file: bool
        self.use_print: bool
        self.log_path, self.use_file, self.use_print = self.get_log_settings()
        self.logger: Logger = Logger(self.log_path, self.use_file, self.use_print)

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='UTF8') as file:
            return yaml.safe_load(file)

    def yaml_error(self, msg: str) -> None: # YAML 파일 읽기 실패, YAML 문법 오류 발생 시 실행
        self.help_logger: Logger = Logger(self.yaml_log, True, True) 
        self.help_logger.exception(msg, f"[{self.__class__.__name__}] ")

    def get_log_settings(self) -> Optional[Tuple[str, bool, bool]]:
        try:
            config: Dict[str, Any] = self.load_yaml(self.img_config)
                
            log_path: str = config['log_settings']['path']
            use_file: bool = config['log_settings']['use_file']
            use_print: bool = config['log_settings']['use_print']
            
            if not isinstance(use_file, bool) or not isinstance(use_print, bool):
                raise ValueError("use_file and use_print must be a boolean value.")
            
            if not os.path.exists(os.path.dirname(log_path)):
                log_dir = os.path.dirname(log_path)
                os.makedirs(log_dir)
            
            return log_path, use_file, use_print
        
        except ValueError as ve:
            self.yaml_error(f"Occur value error. Check the value--> {ve}")
        except FileNotFoundError as fnf:
            self.yaml_error(f"Unavailable file. Check the yaml file--> {fnf}")
        except KeyError as ke:
            self.yaml_error(f"Using the wrong yaml key. Check the yaml file--> {ke}")
        except Exception as e:
            self.yaml_error(f"Check the error log--> {e}")
            
        return None

    def get_img_path(self) -> Optional[Tuple[str, Dict[str, str]]]:
        try:
            config: Dict[str, str] = self.load_yaml(self.img_config)
            
            for path in config['3Dfile_paths']:
                if self.check_path(path['path']):
                    self.logger.info(f'Successfully read {path["type"]} from {path["path"]}')
                    return path['path'], config
            # for path in config['3Dfile_paths']: # PCD 파일 또는 PLY 파일을 읽는다
            #     if path['type'] == 'pcd_file' and self.check_path(path['path']):
            #         self.logger.info(f'Successfully read {path["type"]} from {path["path"]}')
            #         return path['path'], config # PCD 파일 경로, YAML 설정 값
                
            #     elif path['type'] == 'ply_file' and self.check_path(path['path']):
            #         self.logger.info(f'Successfully read {path["type"]} from {path["path"]}')
            #         return path['path'], config # PLY 파일 경로, YAML 설정 값

            raise FileNotFoundError(f"Check the {path['type']} and {path['path']}")
        
        except ValueError as ve:
            self.logger.exception(f"Occur value error. Check the value--> {ve}")
        except FileNotFoundError as fnf:
            self.logger.exception(f"Unavailable image file. Check the yaml file--> {fnf}")
        except KeyError as ke:
            self.logger.exception(f"Using the wrong yaml key. Check the yaml file--> {ke}")
        except Exception as e:
            self.logger.exception(f"Check the error log--> {e}")

    def check_path(self, path: str, exit: bool=True) -> bool:
        if not path:
            self.empty_path()
            return False
        
        if not os.path.exists(os.path.dirname(path)):
            result = self.directory_not_exist(path, exit)
            return result
        
        self.logger.info(f"Correct path: {path}")
        return True

    def empty_path(self) -> None:
        self.logger.error(
            f"[{inspect.currentframe().f_back.f_code.co_name}] "
            f"Path is empty", 
            f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
        )

    def directory_not_exist(self, path: str, exit: bool) -> bool:
        if exit: # 경로가 존재하지 않으면 프로그램 종료
            self.logger.error(
                f"[{inspect.currentframe().f_back.f_code.co_name}] "
                f"Directory does not exist: {path}", 
                f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
            )
            return False
        else: # 경로가 존재하지 않아도 프로그램을 종료하지 않는다
            path = os.path.dirname(path)
            os.makedirs(path)
            self.logger.warning(
                f"[{inspect.currentframe().f_back.f_code.co_name}] "
                f"An existing path does not exist. Create a new path: {path}", 
                f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
            )
            return True