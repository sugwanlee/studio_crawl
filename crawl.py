from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
# 옵션 설정 (필수는 아님)
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def crawl_youtube(id, password):
    # 드라이버 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 웹 페이지 열기
    driver.get('https://www.youtube.com/channel_switcher')

    # WebDriverWait 객체 생성 (최대 10초 대기)
    wait = WebDriverWait(driver, 10)

    # 이메일 입력 필드가 나타날 때까지 대기
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(id)

    # '다음' 버튼이 클릭 가능할 때까지 대기 후 클릭
    next_button = wait.until(EC.element_to_be_clickable((By.ID, "identifierNext")))
    next_button.click()

    # 비밀번호 입력 필드가 나타날 때까지 대기
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
    password_input.send_keys("tnrhks12!@")

    # 로그인 버튼 클릭
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "passwordNext")))
    login_button.click()

    # 채널 목록이 로드될 때까지 대기
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-account-item-renderer")))

    # 모든 채널 정보 가져오기
    channels = driver.find_elements(By.CSS_SELECTOR, "ytd-account-item-renderer")
    channel_list = []

    for channel in channels:
        try:
            channel_name = channel.find_element(By.CSS_SELECTOR, "#channel-title").text
            channel_id = channel.find_element(By.CSS_SELECTOR, "yt-formatted-string[secondary]").text
            channel_list.append({
                'name': channel_name,
                'id': channel_id,
                'element': channel
            })
        except:
            continue

    print("채널 목록:")
    for channel in channel_list:
        print(f"이름: {channel['name']}, ID: {channel['id']}")

    # 각 채널을 순서대로 클릭
    for channel in channel_list:
        try:
            print(f"\n{channel['name']} 채널로 전환 중...")
            # 채널 전환 페이지로 이동
            driver.get('https://www.youtube.com/channel_switcher')
            time.sleep(2)  # 페이지 로딩 대기
            
            # 채널 목록이 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-account-item-renderer")))
            
            # 해당 채널 찾기
            channel_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//yt-formatted-string[@id='channel-title'][text()='{channel['name']}']/ancestor::tp-yt-paper-icon-item")
            ))
            
            # 채널 클릭
            channel_element.click()
            print(f"{channel['name']} 채널로 전환 완료")

            # 채널 전환 후 대기
            avatar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.style-scope.yt-img-shadow")))
            avatar.click()

            # YouTube 스튜디오 링크 클릭
            studio_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[@id='label'][text()='YouTube 스튜디오']/ancestor::a")))
            studio_link.click()

            # # '계속' 버튼 클릭
            # continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#dismiss-button")))
            # continue_button.click()

            # 분석 메뉴 클릭
            analytics_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.menu-item-link[href*='/analytics/tab-overview']")))
            analytics_menu.click()

            # 고급 모드 클릭
            advanced_mode = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='고급 모드']")))
            advanced_mode.click()

            # 측정항목 추가 버튼 클릭
            add_metric = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-icon-button#add-metric-icon")))
            add_metric.click()

            # 유효 조회수 메트릭 선택
            engaged_views = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-item#ENGAGED_VIEWS")))
            engaged_views.click()

            # 내보내기 버튼 클릭
            export_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-icon-button#export-button")))
            export_button.click()

            # CSV 내보내기 옵션 클릭
            csv_export = wait.until(EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[text()='쉼표로 구분된 값(.csv)']")))
            csv_export.click()

            # 채널 전환 후 대기
            time.sleep(5)
            
        except Exception as e:
            print(f"채널 전환 중 오류 발생: {str(e)}")
            continue

    time.sleep(3)
    # 예: 검색창에 키워드 입력

