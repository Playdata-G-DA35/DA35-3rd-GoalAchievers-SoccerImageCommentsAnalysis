# 텍스트 정제
# Okt
from konlpy.tag import Okt
import re

def cleaning_okt(comments):

    # 특수문자 제거
    comments = re.sub(r'[^a-zA-Z\s가-힣]', '', comments)

    # 토큰화 및 품사부착
    okt = Okt()
    okt_tokens = okt.pos(comments, stem=True, norm=True)
    comm_tokens = [word for word, pos in okt_tokens if pos in ['Verb', 'Noun', 'Adjective']]

    # 불용어 사전을 만들어서 불용어 제거
    with open('project\stopword.txt', "rt", encoding = "utf-8") as fo:
        stopwords = fo.read().split("\n")
    result = [word for word in comm_tokens if word not in stopwords]

    return result
