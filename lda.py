# -*- coding: utf-8 -*-
"""
Created on Sun june 26 19:49:24 2018
@author: Administrator
"""
import pickle
from gensim.models import LdaModel
from gensim.models import TfidfModel
from gensim.test.utils import get_tmpfile
from gensim.similarities import MatrixSimilarity
import pickle
f_dict= open('dict_corpus.pkl','rb')
dict_corpus=pickle.load(f_dict)
dictionary=dict_corpus[0]
corpus=dict_corpus[1]
num_list=dict_corpus[3]
train_list=dict_corpus[-1]
#此程序大概需要三个小时
def lda():
    #使用数字语料生成TFIDF模型
    #print(corpus)
    tfidfModel = TfidfModel(corpus)
    tfidfModel.save('TFIDF.model')
    #把全部语料向量化成TFIDF模式，这个tfidfModel可以传入二维数组
    tfidfVectors = tfidfModel[corpus]
    #建立索引并保存
    #indexTfidf = MatrixSimilarity(tfidfVectors)
    #通过TFIDF向量生成LDA模型，id2word表示编号的对应词典，num_topics表示主题数，
    lda = LdaModel(tfidfVectors, id2word=dictionary, num_topics=200,iterations=100)
    #把模型保存下来
    lda.save("200Topic.model")
    #把所有TFIDF向量变成LDA的向量
    corpus_lda = lda[tfidfVectors]
    #建立索引，把LDA数据保存下来
    #MatrixSimilarity(corpus, num_features,num_best)
    indexLDA = MatrixSimilarity(corpus_lda)
    indexLDA.save("200Topic.idx")
    
if __name__=='__main__':
   lda()
