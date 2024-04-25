# 텍스트 정제
# WordPiece
from tokenizers import Tokenizer
from tokenizers.models import WordPiece
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import WordPieceTrainer
import time
import re

def cleaning_wp(comments):
    # 특수문자 제거
    comments = re.sub(r'[^a-zA-Z\s가-힣]', '', comments)
    
    file_name = 'project/comments.txt'
    with open(file_name, 'wt', encoding='utf-8') as fw:
        fw.write(comments)


    # 토크나이저 알고리즘 객체를 넣어서 tokenizer 생성
    wp_tokenizer = Tokenizer(WordPiece(unk_token='[UNK]'))
    # Pre tokenizer 설정. (1차 토큰화 작업단위)
    wp_tokenizer.pre_tokenizer = Whitespace()
    # Trainer 생성 -> 어휘사전 어떻게 만들지 설정
    trainer = WordPieceTrainer(vocab_size=20000)

    batch_size=500
    current_batch=[]
    text_path = 'project/comments.txt'

    with open(text_path, 'rt', encoding='utf-8') as fr:
        s=time.time()

        for line in fr:
            current_batch.append(line)
            if len(current_batch) == batch_size:
                wp_tokenizer.train_from_iterator(current_batch, trainer)

        wp_tokenizer.train_from_iterator(current_batch, trainer)
        
        e=time.time()

    print(f'WordPiece tokenize 걸린시간 : {e-s}초')
    
    # saved_path='comments.json'
    # wp_tokenizer.save(saved_path)
    # saved_tokenizer = Tokenizer.from_file(saved_path)

    with open('project/comments.txt', 'rt', encoding='utf-8') as fr:
        comments = fr.read()
        
    output = wp_tokenizer.encode(comments)
    comm_tokens = output.tokens


    # 불용어 사전을 만들어서 불용어 제거
    f = open(r'project\stopword.txt', "rt", encoding = "utf-8")
    stopwords = f.read().split("\n")
    result = [word for word in comm_tokens if word not in stopwords]
    
    return result
