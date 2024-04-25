from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawling(url):
    service = Service(executable_path = ChromeDriverManager().install())
    # option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()

    # 유튜브 영상 사이트로 이동
    browser.get(url) # 호주전
    # browser.get("https://www.youtube.com/watch?v=FBynfiRGdlc") # 사우디전
    time.sleep(5)

    # 현재 페이지의 높이 조회 -> javascript***
    scroll_pane_height = browser.execute_script("return document.documentElement.scrollHeight") 
    # 댓글창 로딩될 만큼 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight * 0.1)")
    time.sleep(2)

    cnt = 0
    while True:
        # 스크롤 내리기
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
        # 이동 후 height 를 조회
        time.sleep(3)
        new_scroll_pane_height = browser.execute_script(
            "return document.documentElement.scrollHeight"
        )
        # 이전 높이와 이동 후 높이가 같다면 
        if scroll_pane_height == new_scroll_pane_height: 
            break
        scroll_pane_height = new_scroll_pane_height
        cnt += 1

    # 조회 (크롤링)
    time.sleep(2)
    comments_tag = browser.find_elements(By.CSS_SELECTOR,"#content-text > span") # css selector

    # 댓글 리스트 
    comment_list=[]

    for tag in comments_tag:
        comment_list.append(tag.text)
    print('crawling len : ', len(comment_list))
    
    browser.close()

    return comment_list
