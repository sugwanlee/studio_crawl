from crawl import crawl_youtube
from zip_to_folder import extract_zip_files
from data_sum import collect_table_data
from upload_db import upload_csv_to_db
import time
import os
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")

id = os.getenv("YOUTUBE_ID")
password = os.getenv("YOUTUBE_PASSWORD")

def main():
    # 크롤링 재시도 횟수
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"1. YouTube 데이터 크롤링 시작... (시도 {retry_count + 1}/{max_retries})")
            crawl_youtube(id, password)
            print("크롤링 완료!")
            break  # 성공하면 while 루프 종료
            
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"크롤링 실패: {str(e)}")
                print(f"5초 후 재시도합니다...")
                time.sleep(5)
            else:
                print("최대 재시도 횟수를 초과했습니다. 프로그램을 종료합니다.")
                return
    
    print("\n2. ZIP 파일 압축 해제 시작...")
    extracted_folders = extract_zip_files(base_path)
    if not extracted_folders:
        print("압축 해제할 파일이 없습니다.")
        return
    print("압축 해제 완료!")
    
    print("\n3. 표 데이터 수집 시작...")
    result_folder = collect_table_data(extracted_folders)
    if not result_folder:
        print("표 데이터 수집 실패!")
        return
    print(f"표 데이터 수집 완료! 결과 폴더: {result_folder}")
    
    print("\n4. 데이터베이스 업로드 시작...")
    upload_csv_to_db(result_folder)
    print("데이터베이스 업로드 완료!")

if __name__ == "__main__":
    main()

