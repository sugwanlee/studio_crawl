import os
import glob
import shutil
from datetime import datetime

def collect_table_data(extracted_folders):
    if not extracted_folders:
        print("압축 해제된 폴더가 없습니다.")
        return None
        
    # 오늘 날짜를 YYYY-MM-DD 형식으로 가져오기
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 결과를 저장할 폴더 생성 (첫 번째 폴더의 상위 디렉토리에 생성)
    base_dir = os.path.dirname(extracted_folders[0])
    output_dir = os.path.join(base_dir, f'table_data_{today}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 각 압축 해제된 폴더에서 '표 데이터.csv' 파일 찾기
    for folder in extracted_folders:
        try:
            # 폴더 내에서 '표 데이터.csv' 파일 찾기
            csv_file = os.path.join(folder, '표 데이터.csv')
            if os.path.exists(csv_file):
                # 폴더 이름 가져오기 (채널 이름)
                folder_name = os.path.basename(folder)
                # 새로운 파일 이름 생성 (채널명_표 데이터.csv)
                new_file_name = f"{folder_name}_표 데이터.csv"
                # 대상 경로 생성
                target_path = os.path.join(output_dir, new_file_name)
                
                # 파일 복사
                shutil.copy2(csv_file, target_path)
                print(f"파일이 복사되었습니다: {new_file_name}")
            else:
                print(f"'{folder}' 폴더에서 '표 데이터.csv' 파일을 찾을 수 없습니다.")
                
        except Exception as e:
            print(f"파일 복사 중 오류 발생: {str(e)}")
    
    print(f"\n모든 '표 데이터.csv' 파일이 {output_dir} 폴더에 복사되었습니다.")
    return output_dir  # 결과 폴더 경로 반환

if __name__ == "__main__":
    # 소스 폴더 경로 입력
    source_folder = input("CSV 파일이 있는 폴더 경로를 입력하세요: ")
    collect_table_data(source_folder)
