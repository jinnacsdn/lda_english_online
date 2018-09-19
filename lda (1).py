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
import time
from logger import get_logger
log_file_name=os.path.basename(__file__).split('.',1)[0]+'.log'
# Save params
if os.path.exists(log_file_name) is False or os.path.getsize(log_file_name)/1024<1:
   logger = get_logger(log_file_name,mode='a')
else:
   #����ɾ����ǰ����־
   logger = get_logger(log_file_name)

start=time.time()
f_dict= open('dict_corpus.pkl','rb')
dict_corpus=pickle.load(f_dict)
dictionary=dict_corpus[0]
corpus=dict_corpus[1]
url_list=dict_corpus[2]
num_list=dict_corpus[3]
string_list=dict_corpus[4]
train_list=dict_corpus[-1]
logger.info("{}".format(len(url_list)))
logger.info("{}".format(len(num_list)))
logger.info("{}".format(len(string_list)))
logger.info("{}".format(len(train_list)))
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
   elapsed=(time.time()-start)/60/60
   logger.info("Time used:{} hours".format(elapsed))
