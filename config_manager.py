import yaml
import os
import inspect
from typing import Optional, Tuple, Dict, Any

from logger import Logger

class ConfigFileManager:
    def __init__(self) -> None:
        """YAML 설정 파일 경로 설정 및 YAML 에러용 로그 경로 설정을 한다.
        로그 클래스 사용을 위해 YAML 파일에 지정된 로그 경로, 로그 파일 기록 여부, 로그 출력 여부
        3가지 파라미터 값을 get_log_settings를 실행하여 가져온다.
        3가지 파라미터들을 사용하여 Logger 클래스 인스턴스를 생성한다.

        """
        self.img_config: str = 'config/image.yaml'  # 설정 파일 경로
        self.yaml_log: str = 'log/yaml_error.log'  # YAML 에러용 로그 경로
        self.log_path: str
        self.use_file: bool
        self.use_print: bool
        self.log_path, self.use_file, self.use_print = self.get_log_settings()
        self.logger: Logger = Logger(self.log_path, self.use_file, self.use_print)

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        """YAML 설정 파일을 읽는다.
        
        Args:
            file_path : 지정된 설정 파일 경로.
        Returns:
            YAML 설정 파라미터들.

        """
        with open(file_path, 'r', encoding='UTF8') as file:
            return yaml.safe_load(file)

    def yaml_error(self, msg: str) -> None: # YAML 파일 읽기 실패, YAML 문법 오류 발생 시 실행
        """설정 파일 경로에 문제가 있어 YAML 파일을 읽지 못하거나, YAML 문법에 오류가 있을 때
        발생하는 에러를 기록하기 위한 logger. get_log_settings 메소드 실행 전에 발생하는 에러들을 기록한다.
        로그 파일 기록과 터미널에 출력 기능은 반드시 한다.
        
        Args:
            msg : 로그 파일에 저장 또는 터미널에 출력할 메세지.
        Returns:
            없음.

        """
        self.help_logger: Logger = Logger(self.yaml_log, True, True) 
        self.help_logger.exception(msg, f"[{self.__class__.__name__}] ")

    def get_log_settings(self) -> Optional[Tuple[str, bool, bool]]:
        """YAML 설정 파일에 지정된 로그 세팅 관련 파라미터들을 불러온다.
        로그 파일 경로가 존재하지 않는 경우 디렉토리를 자동으로 생성 후 해당 위치에 로그 파일을 저장한다.
        YAML 문법, Key 값, 파라미터 값에 문제가 있는 경우 예외 처리를 사용해 로깅한다.
        
        Args:
            없음.
        Returns:
            기록할 로그 파일 경로, 로그 파일 기록 여부, 터미널에 출력 여부 반환.
        Raises:
            use_file, use_print 값이 bool 아닌 경우 에러 발생
            
        """
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
            self.yaml_error(f"Occur log path value error. Check the value--> {ve}")
        except FileNotFoundError as fnf:
            self.yaml_error(f"Unavailable file. Check the log file--> {fnf}")
        except KeyError as ke:
            self.yaml_error(f"Occur key error. Check the log file--> {ke}")
        except Exception as e:
            self.yaml_error(f"Check the error yaml_error log--> {e}")
            
        return None

    def get_img_path(self) -> Optional[Tuple[str, Dict[str, str]]]:
        """YAML 설정 파일로 부터 PCD 또는 PLY 파일 경로를 획득한다.
        file_exist 메소드를 사용하여 파일 존재 여부를 확인한다.
        
        Args:
            없음.
        Returns:
            3D 파일 경로, YAML 설정 값들 반환.
        Raises:
            3D 파일 경로에 문제가 있는 경우 또는 해당 경로에 파일이 없는 경우.
            
        """        
        try:
            config: Dict[str, str] = self.load_yaml(self.img_config)
            
            for path in config['3Dfile_paths']:
                if self.file_exist(path['path']):
                    self.logger.info(f'Successfully read {path["type"]} from {path["path"]}')
                    return path['path'], config

            raise FileNotFoundError(f"Check the {path['type']} and {path['path']}")
        
        except ValueError as ve:
            self.logger.exception(f"Occur img path value error. Check the value--> {ve}")
        except FileNotFoundError as fnf:
            self.logger.exception(f"Unavailable image file. Check the yaml file--> {fnf}")
        except KeyError as ke:
            self.logger.exception(f"Using the wrong yaml key. Check the yaml file--> {ke}")
        except Exception as e:
            self.logger.exception(f"Check the error total log--> {e}")

    def file_exist(self, path: str) -> bool:
        """YAML 설정 파일로 부터 PCD 또는 PLY 파일 경로를 획득한다.
        file_exist 메소드를 사용하여 파일 존재 여부를 확인한다.
        로그 파일 기록을 용이성을 위한 [file_exist 호출 클래스] [file_exist 호출 메소드] 로그 포맷 추가.
        error 메소드에 파라미터를 전달할 때는 [file_exist 호출 메소드] 메세지, [file_exist 호출 클래스]
        순으로 2가지를 전달한다.
        
        Args:
            path : 확인하고 싶은 파일 경로.
        Returns:
            파일이 존재하는 경우 True, 파일이 존재하지 않는 경우 False 반환.
        
        """   
        if os.path.isfile(path):
            self.logger.info(f"File exist: {path}")
            return True
        else:
            self.logger.error(
                f"[{inspect.currentframe().f_back.f_code.co_name}] "
                f"Check the file name", 
                f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
            )
            return False

    def empty_path(self, path: str) -> bool:
        if not path:
            self.logger.error(
                f"[{inspect.currentframe().f_back.f_code.co_name}] "
                f"Path is empty", 
                f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
            )
            return True
        else:
            self.logger.info(f"Correct path: {path}")
            return False

    def directory_exist(self, path: str, make: bool) -> bool:
        """경로 존재 여부를 확인한다.
        file_exist 메소드를 사용하여 파일 존재 여부를 확인한다.
        경로 확인 후 로그에 기록한다.
        로그 파일 기록을 용이성을 위한 [file_exist 호출 클래스] [file_exist 호출 메소드] 로그 포맷 추가.
        error 메소드에 파라미터를 전달할 때는 [directory_exist 호출 메소드] 메세지, [directory_exist 호출 클래스]
        순으로 2가지를 전달한다.
        
        Args:
            path : 확인하고 싶은 경로.
            make : True인 경우 path에 맞는 디렉토리 생성, False인 경우 디렉토리 생성 안함.
        Returns:
            디렉토리 존재, 또는 디렉토리 생성한 경우 True, 디렉토리 생성하지 않는 경우 False 반환.
        
        """   
        if not os.path.exists(os.path.dirname(path)):
            if make: # path에 맞는 디렉토리 생성
                path = os.path.dirname(path)
                os.makedirs(path)
                self.logger.warning(
                    f"[{inspect.currentframe().f_back.f_code.co_name}] "
                    f"An existing path does not exist. Create a new path: {path}", 
                    f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
                )
                return True
            else: # 디렉토리 생성 안함
                self.logger.error(
                    f"[{inspect.currentframe().f_back.f_code.co_name}] "
                    f"Directory does not exist: {path}", 
                    f"[{inspect.currentframe().f_back.f_locals['self'].__class__.__name__}] "
                )
                return False
        else: # 경로에 맞는 디렉토리 존재
            return True