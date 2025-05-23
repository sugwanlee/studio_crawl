import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime

def create_table(cursor):
    # 테이블 생성 쿼리
    create_table_query = """
    CREATE TABLE IF NOT EXISTS youtube_analytics (
        id SERIAL PRIMARY KEY,
        channel_name VARCHAR(255),
        content_type VARCHAR(255),
        video_title VARCHAR(500),
        publish_time TIMESTAMP,
        video_length VARCHAR(50),
        valid_views INTEGER,
        views INTEGER,
        watch_time_hours DECIMAL(10,2),
        subscribers INTEGER,
        impressions INTEGER,
        impression_click_rate DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)

def upload_csv_to_db(csv_folder_path):
    try:
        # PostgreSQL 연결
        conn = psycopg2.connect(
            host="localhost",
            database='studio_db',
            user="postgres",
            password='0000'
        )
        cursor = conn.cursor()

        # 테이블 생성
        create_table(cursor)
        
        # CSV 파일 목록 가져오기
        csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
        
        if not csv_files:
            print("CSV 파일을 찾을 수 없습니다.")
            return
        
        # 각 CSV 파일 처리
        for csv_file in csv_files:
            try:
                # 채널 이름 추출 (파일명에서)
                channel_name = csv_file.split('_표 데이터.csv')[0]
                file_path = os.path.join(csv_folder_path, csv_file)
                
                # CSV 파일 읽기
                df = pd.read_csv(file_path)
                
                # '합계' 행 제외
                df = df[df['콘텐츠'] != '합계']
                
                # 데이터 삽입
                for _, row in df.iterrows():
                    insert_sql = """
                    INSERT INTO youtube_analytics 
                    (channel_name, content_type, video_title, publish_time, video_length,
                     valid_views, views, watch_time_hours, subscribers, impressions, impression_click_rate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    # 데이터 변환
                    publish_time = pd.to_datetime(row['동영상 게시 시간']) if pd.notna(row['동영상 게시 시간']) else None
                    valid_views = int(row['유효 조회수']) if pd.notna(row['유효 조회수']) else 0
                    views = int(row['조회수']) if pd.notna(row['조회수']) else 0
                    watch_time = float(row['시청 시간(단위: 시간)']) if pd.notna(row['시청 시간(단위: 시간)']) else 0.0
                    subscribers = int(row['구독자']) if pd.notna(row['구독자']) else 0
                    impressions = int(row['노출수']) if pd.notna(row['노출수']) else 0
                    click_rate = float(row['노출 클릭률 (%)']) if pd.notna(row['노출 클릭률 (%)']) else 0.0
                    
                    cursor.execute(insert_sql, (
                        channel_name,
                        row['콘텐츠'],
                        row['동영상 제목'],
                        publish_time,
                        row['길이'],
                        valid_views,
                        views,
                        watch_time,
                        subscribers,
                        impressions,
                        click_rate
                    ))
                
                print(f"{csv_file} 파일의 데이터가 성공적으로 업로드되었습니다.")
                
            except Exception as e:
                print(f"{csv_file} 파일 처리 중 오류 발생: {str(e)}")
                continue
        
        # 변경사항 저장
        conn.commit()
        print("모든 데이터가 성공적으로 업로드되었습니다.")
        
    except Exception as e:
        print(f"데이터베이스 연결 또는 처리 중 오류 발생: {str(e)}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    # CSV 파일이 있는 폴더 경로 입력
    csv_folder = input("CSV 파일이 있는 폴더 경로를 입력하세요: ")
    upload_csv_to_db(csv_folder)
