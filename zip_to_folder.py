import os
import zipfile
from datetime import datetime
import glob

def extract_zip_files(zip_folder_path):
    # 입력받은 폴더 경로가 존재하는지 확인
    if not os.path.exists(zip_folder_path):
        print(f"입력한 폴더 경로가 존재하지 않습니다: {zip_folder_path}")
        return None

    # 오늘 날짜를 YYYY-MM-DD 형식으로 가져오기
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 지정된 폴더에서 '콘텐츠'로 시작하고 오늘 날짜가 포함된 zip 파일 찾기
    zip_pattern = os.path.join(zip_folder_path, f'콘텐츠 *_{today} *.zip')
    zip_files = glob.glob(zip_pattern)
    
    if not zip_files:
        print(f"오늘 날짜({today})가 포함된 zip 파일을 찾을 수 없습니다.")
        return None
    
    extracted_folders = []  # 압축 해제된 폴더 경로들을 저장할 리스트
    
    # 각 zip 파일 압축 해제
    for zip_file in zip_files:
        try:
            # 압축 해제할 디렉토리 이름 생성 (zip 파일 이름에서 .zip 제외)
            extract_dir = os.path.splitext(zip_file)[0]
            
            # 디렉토리가 없으면 생성
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
            
            # zip 파일 압축 해제
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print(f"{zip_file} 파일의 압축이 {extract_dir} 디렉토리에 해제되었습니다.")
            extracted_folders.append(extract_dir)  # 압축 해제된 폴더 경로 저장
            
        except Exception as e:
            print(f"파일 압축 해제 중 오류 발생: {str(e)}")
    
    return extracted_folders  # 압축 해제된 폴더 경로 리스트 반환

extract_zip_files("/Users/isugwan/Downloads")