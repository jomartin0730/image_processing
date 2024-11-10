# 목표
3D 포인트 클라우드 데이터 처리 및 2D 투영 시스템 개발  

<br>

## 필요 라이브러리 설치
```bash
pip install pyyaml open3d numpy matplotlib
```
<br>

## Python 버전
Python 3.10.11   


<br>

## 프로젝트 실행 방법
```
git clone https://github.com/jomartin0730/image_processing.git
cd image_processing
python3 main.py
```
<br>

## 주요 Class와 Function
- 설정 파일 관리 클래스(ConfigFileManager)
- 3D 데이터 관리 클래스(DataManager)
- 3D 데이터 처리 알고리즘 클래스(DataProcessing)
- 로거 클래스(Logger)
설정 파일 읽기 -> 로거 클래스 등록 -> 데이터 불러오기 -> 데이터 처리 -> 이미지 저장


<br>

## 프로젝트 구조
- 프로젝트 구조
``` 
    📦image_processing
     ┣ 📂config
     ┃ ┗ 📜image.yaml
     ┣ 📂data
     ┃ ┣ 📜sample_data.pcd
     ┃ ┗ 📜sample_data.ply
     ┣ 📂log
     ┃ ┗ 📜total.log
     ┃ ┗ 📜yaml_error.log
     ┣ 📂result
     ┃ ┣ 📜depth_map.png
     ┃ ┗ 📜heat_map.png
     ┣ 📜config_manager.py
     ┣ 📜data_manager.py
     ┣ 📜data_processing.py
     ┣ 📜logger.py
     ┣ 📜main.py
     ┣ 📜README.md
     ┗ 📜unit_test.py
```
- config
  - YAML 설정 파일이 있는 디렉토리
- data
  - 포인트 클라우드 파일이 있는 디렉토리
- log
  - 로그 파일 저장 디렉토리
- result
  - 생성된 2D 이미지 파일 저장 디렉토리  
- 주요 클래스
  - **ConfigFileManager(설정 파일 관리 클래스)**
    - yaml_error
      - YAML 파일 읽기 실패, YAML 문법 오류 발생 시 실행
    - get_img_path
      - pcd 또는 ply 파일 경로 리턴
      - YAML 파일 파라미터 값들 리턴
      - 예외 처리를 사용하여 에러 case 관리
    - get_log_settings
      - 로그 경로, 파일 로그 사용 여부, Print 사용 여부 값들을 리턴
      - 예외 처리를 사용하여 에러 case 관리
    - check_path
      - 지정한 파일 경로 확인


  - **DataManager(3D 데이터 관리 클래스)**
    - get_depths
      - X 좌표의 최대, 최소 깊이 계산
    - save_image
      - depth, heat 맵 저장
      - 경로가 지정되지 않으면 저장하지 않음


  - **DataProcessing(3D 데이터 처리 알고리즘 클래스)**
    - remove_noise
      - statistical 또는 radius 알고리즘을 사용하여 노이즈 제거
      - 위의 2가지 알고리즘 이외에는 에러로 간주하여 예외 처리를 통해 관리
    - project_to_2d
      - 3D 이미지를 벡터 방향에 따라 투영 후 2D 배열로 변환
      - 투영된 이미지의 개수가 홀수인 경우 마지막 포인트 제거
    - create_depth_map
      - 투영된 포인트들을 2D depth map으로 생성
    - create_heat_map
      - 투영된 포인트들을 2D heat map으로 생성
      - 붉은색 사용


  - **Logger(로거 클래스)**
    - setup_logger
      - 설정 파일 세팅에 따라 로그 파일에 저장 또는 프린트로 출력 가능
      - 로그 포맷
        - 일반 : 시간 [로그 레벨] 메세지
        - check_path 메소드에서 error 발생 시 : 시간 [로그 레벨] [클래스 명] [메소드 명] 메세지
        - main에서 error 발생 시 : 시간 [로그 레벨] [__main__] 메세지


  - **TestDataProcessing(단위 테스트 클래스)**
    - DataProcessing의 주요 method들에 대한 단위 테스트
  

