from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os 
from datetime import datetime
import time

service = Service(executable_path = ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

# implicit wait 
browser.implicitly_wait(5) # 로딩될 때까지 최대 5초 대기 
browser.maximize_window()

# 유튜브 영상 사이트로 이동
browser.get('https://www.youtube.com/watch?v=kW_z-NMuZIU') # 호주전
# browser.get("https://www.youtube.com/watch?v=FBynfiRGdlc") # 사우디전
time.sleep(5)

# 현재 페이지의 높이 조회 -> javascript***
scroll_pane_height = browser.execute_script("return document.documentElement.scrollHeight") 
# 댓글창 로딩될 만큼 스크롤 내리기
browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight * 0.1)")
time.sleep(2)

# 댓글 리스트 
comment_list=[]

while True:

    # 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
    # 이동 후 height 를 조회
    time.sleep(2)
    new_scroll_pane_height = browser.execute_script(
        "return document.documentElement.scrollHeight"
    )
    # 이전 높이와 이동 후 높이가 같다면 
    if scroll_pane_height == new_scroll_pane_height: 
        break
    scroll_pane_height = new_scroll_pane_height

    # 조회 (크롤링)
    time.sleep(1)
    comments_tag = browser.find_elements(By.CSS_SELECTOR,"#content-text > span") # css selector
    for tag in comments_tag:  
        comment_list.append(tag.text)

browser.close()

# 크롤링한 댓글 파일 저장 
# os.makedirs("project",exist_ok=True)
d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

file_name = f'comments_{d}.txt'

with open(file_name, 'w',encoding='utf-8') as file:
    file.write(' '.join(comment_list))

comments = str(comment_list).replace("\n"," ")
print(len(comments))



import re
import konlpy
from konlpy.tag import Okt

# 특수문자, 숫자 제거 
comments = re.sub(r"[^a-zA-Z\s가-힣]", "", comments) # 패턴, 바꿀 문자열, string

# 토큰화 및 품사부착 (Okt)
okt = Okt()
okt_tokens = okt.pos(comments, stem = True) #원형복원 # 비속어 처리 

# 명사 동사만추출
comm_tokens = [word for word, pos in okt_tokens if pos in ['Verb','Noun']] # 명사만 추출할 시 Noun쓰면 됨
comm_tokens[:20]


# 선수이름

# 불용어 사전을 만들어서 불용어 제거
stop_words = '이 은 에 어제 엄청 진짜 있다 없다 저기 서 근데 아니 가 을 를 도 . 들 의 이다 하다 너무 잘 .. ... 오다 아니다 뛰다\
        때 로 까지 에서 정말 오다 같다 ㅋㅋㅋ 한 안 적 조 ! 는 다 되다 않다 것 만 못 성 으로 더 , ? 4 보고 우리 보다 하고\
        이번 의 끝 자다 들다 만들다 크다 왜 수 그 거 모두 앞 국 게 보 분 하나 해주다 개 알다 나오다 주다'


stop_words_list = set(stop_words.split(' '))

result = [word for word in comm_tokens if not word in stop_words_list]
print(len(result))


from nltk import Text
text = Text(result, name = "호주전")


# 빈도수 선 그래프 시각화
import matplotlib.pyplot as plt

#한글 설정
plt.rcParams['font.family'] = 'malgun gothic'
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(12,5))  # 선그래프 가로로 길게
plt.title('호주전')
text.plot(30)
plt.show()

# 그래프를 이미지로 저장
os.makedirs("project/plot",exist_ok=True)
plt.savefig(f'project/plot/plot_{d}.png')


### 빈도수 관련 분석
fd = text.vocab()
print("고유 토큰 개수:",fd.B())
print('총 토큰 수:', fd.N())
print('가장 많이 나온 토큰:', fd.max())
print('손흥민의 빈도수:', fd.get('손흥민')) 
print('황희찬의 빈도수:', fd.get('황희찬')) 
print(f'가장 많이 나온 토큰({fd.max()})의 빈도수: {fd.get(fd.max())}')
print(f"가장 많이 나온 토큰의 총 토큰수 대비 비율: {fd.freq(fd.max())* 100:.2f}%")


## WordCloud
from wordcloud import WordCloud

wc = WordCloud(
    font_path = r"c:\Winddows\Fonts\malgun.ttf",
    max_words = 100,
    min_font_size = 1,
    max_font_size = 50,
    relative_scaling = 0.5, 
)
# 파일 저장 
# 출력 이미지 
word_cloud_img = wc.generate_from_frequencies(fd)

os.makedirs("project/wordcloud",exist_ok=True)
wc.to_file(f"project/wordcloud/aus_wc_{d}.png")

plt.figure(figsize= (10,10))
plt.imshow(word_cloud_img)