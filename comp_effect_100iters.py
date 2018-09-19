# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 18:50:29 2018
@author: chenzhikuo
"""

import json
import re
import pickle
import os
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import random
data_list=[]
f_dict= open('dict_corpus.pkl','rb')
dict_corpus=pickle.load(f_dict)
dictionary=dict_corpus[0]
corpus=dict_corpus[1]
train_list=dict_corpus[-1]
coherence_list=[]
def cal_iter_coher(rooddir):
    rootdir = 'iteration'
    list_file = os.listdir(rootdir) #列出文件夹下所有的目录与文件d
    data_list=[]
    f_dict= open('dict_corpus.pkl','rb')
    for i in range(len(list_file)):
        path = os.path.join(rootdir,list_file[i])
        if os.path.isfile(path) and path.endswith('.model'):
           temp_name=path.split('lda_100_',1)[1]   #取后一部分
           Iter=int(temp_name.split('.model',1)[0])  #取前一部分           
           lda_model = LdaModel.load(path)
           cv = CoherenceModel(model=lda_model, texts=train_list, dictionary=dictionary, coherence='c_v')
           coherence=cv.get_coherence()
           coherence_list.append([Iter,coherence])
           print(coherence_list)
    f=open('coherence_iter_100.pkl','wb')
    pickle.dump(coherence_list,f)
if __name__=='__main__':
   i=0
   while i<10:
         random.seed(i)
         lda_model=LdaModel(corpus=corpus,id2word=dictionary,num_topics=700,iterations=100)
         lda_model.save('./iteration100/lda_100_'+str(i)+'.model')  #保存模型
         cv = CoherenceModel(model=lda_model, texts=train_list, dictionary=dictionary, coherence='c_v')
         coherence=cv.get_coherence()
         coherence_list.append([i,coherence])
         i+=1
   print(coherence_list)
   f=open('coherence_iter_100.pkl','wb')
   pickle.dump(coherence_list)
