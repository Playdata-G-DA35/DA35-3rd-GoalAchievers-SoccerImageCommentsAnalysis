# WordCloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def wordcloud(fd):
    wc = WordCloud(
        font_path = "c:\Windows\Fonts\malgun.ttf",
        max_words = 100,
        min_font_size = 1,
        max_font_size = 70,
        relative_scaling = 0.5,
        )

    ## Word Cloud 생성
    word_cloud_img = wc.generate_from_frequencies(fd)

    ## 파일저장
    os.makedirs('project', exist_ok=True)
    wc.to_file('project/aus_wc.png')

    plt.figure(figsize=(10,10))
    plt.axis('off')
    plt.imshow(word_cloud_img)
    plt.show()
