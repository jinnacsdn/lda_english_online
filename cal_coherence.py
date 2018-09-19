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
rootdir = 'model'
list_file = os.listdir(rootdir) #�г��ļ��������е�Ŀ¼���ļ�d
data_list=[]
f_dict= open('dict_corpus.pkl','rb')
dict_corpus=pickle.load(f_dict)
dictionary=dict_corpus[0]
train_list=dict_corpus[-1]
coherence_list=[]
for i in range(len(list_file)):
    path = os.path.join(rootdir,list_file[i])
    if os.path.isfile(path) and path.endswith('.model'):
       temp_name=path.split('lda_',1)[1]   #ȡ��һ����
       num_topic=int(temp_name.split('.model',1)[0])  #ȡǰһ����           
       lda_model = LdaModel.load(path)
       cv = CoherenceModel(model=lda_model, texts=train_list, dictionary=dictionary, coherence='c_v')
       coherence=cv.get_coherence()
       coherence_list.append([num_topic,coherence])
#print(coherence_list)
f=open('coherence.pkl','wb')
pickle.dump(coherence_list,f)                 
