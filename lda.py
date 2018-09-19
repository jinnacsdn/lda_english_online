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
#�˳�������Ҫ����Сʱ
def lda():
    #ʹ��������������TFIDFģ��
    #print(corpus)
    tfidfModel = TfidfModel(corpus)
    tfidfModel.save('TFIDF.model')
    #��ȫ��������������TFIDFģʽ�����tfidfModel���Դ����ά����
    tfidfVectors = tfidfModel[corpus]
    #��������������
    #indexTfidf = MatrixSimilarity(tfidfVectors)
    #ͨ��TFIDF��������LDAģ�ͣ�id2word��ʾ��ŵĶ�Ӧ�ʵ䣬num_topics��ʾ��������
    lda = LdaModel(tfidfVectors, id2word=dictionary, num_topics=200,iterations=100)
    #��ģ�ͱ�������
    lda.save("200Topic.model")
    #������TFIDF�������LDA������
    corpus_lda = lda[tfidfVectors]
    #������������LDA���ݱ�������
    #MatrixSimilarity(corpus, num_features,num_best)
    indexLDA = MatrixSimilarity(corpus_lda)
    indexLDA.save("200Topic.idx")
    
if __name__=='__main__':
   lda()
