# 빈도수 선 그래프 시각화
from nltk import Text
import matplotlib.pyplot as plt

def visualization(result):
    
    text = Text(result, name='호주전')

    plt.rcParams['font.family'] = 'malgun gothic'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10,5))
    plt.title('호주전')
    text.plot(30)
    plt.savefig('project/graph.png')  # 그래프를 이미지 파일로 저장
    plt.show()