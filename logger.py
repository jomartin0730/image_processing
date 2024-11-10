import logging

class Logger:
    def __init__(self, path: str, file: bool, print: bool) -> None:
        self.setup_logger(path, file, print)

    def setup_logger(self, path:str, file: bool, print: bool) -> None:
        """로그의 레벨, 포멧, 핸들러 사용 여부를 설정하는 메소드.
        
        Args:
            path  : 저장할 로그 파일 경로
            file  : 로그 파일 저장 여부 선택.
            print : 터미널에 출력 여부 선택
        Returns:
            없음.
            
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if file:
            file_handler = logging.FileHandler(path)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if print:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str, name: str="") -> None:
        """정상 동작시 실행한다.
        최종 기록 형태는
        
        [name] 메세지 
        
        형태이다.
        
        Args:
            message  : 파일에 기록할 내용.
            name     : 호출된 클래스 또는 함수(main)의 위치.
        Returns:
            없음.
            
        """
        message = name + message
        self.logger.info(message)

    def warning(self, message: str, name: str="") -> None:
        message = name + message
        self.logger.warning(message)

    def error(self, message: str, name: str="") -> None:
        """사용자가 설정한 에러 또는 시스템 에러 발생시 실행한다.
        최종 기록 형태는 
        
        [name] 메세지 
        
        형태이다.
        
        Args:
            message  : 파일에 기록할 내용.
            name     : 호출된 클래스 또는 함수(main)의 위치.
        Returns:
            없음.
            
        """
        message = name + message
        self.logger.error(message) 

    def exception(self, message: str, name: str="") -> None: 
        """사용자가 설정한 에러 또는 시스템 에러 발생시 실행한다.
        Trackback까지 추가로 로그 파일에 기록 또는 터미널에 출력할 수 있다.
        최종 기록 형태는 
        
        [name] 메세지 
        Trackback
        
        형태이다.
        
        Args:
            message  : 파일에 기록할 내용.
            name     : 호출된 클래스 또는 함수(main)의 위치.
        Returns:
            없음.
            
        """
        message = name + message
        self.logger.exception(message) 
