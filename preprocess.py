# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:26:38 2018
此程序大概用时两个小时
@author: chenzhikuo
"""
import json
import re
import pickle
import time
import os
import logging
import numpy as np
from gensim.corpora import Dictionary
from nltk.stem import SnowballStemmer
from logger import get_logger

start=time.time()
log_file_name=os.path.basename(__file__).split('.',1)[0]+'.log'
if os.path.exists(log_file_name) is False or os.path.getsize(log_file_name)/1024<1:
   logger = get_logger(log_file_name,mode='a')
else:
   #否则删除以前的日志
   logger = get_logger(log_file_name)
#将数组转化为出现的次数
def transform(i,dictionary,array,f_times):
    #result_array=np.zeros(len(dictionary))
    num_array = {}
    for word in set(array):
        num_array[word] = array.count(word)
    string=str(i)
    for key in num_array:
        if key in dictionary:
           string+='\x01'+str(dictionary[key])+'\x02'+str(num_array[key])
           #result_array[dictionary[key]]=num_array[key]
    f_times.write(string+'\n')

stemmer=SnowballStemmer('english')
stopwords=open('./dict/en_stopwords.txt','r',encoding='utf8').readlines()
stopwords=[word.strip(' \n') for word in stopwords]
hindi_stopwords=open('./dict/hindi_stopwords.txt','r',encoding='utf8').readlines()
hindi_stopwords=[word.strip(' \n') for word in hindi_stopwords]
stopwords.extend(hindi_stopwords)  #将英语和印地语停止词合并
rootdir = 'video_info'
list_file = os.listdir(rootdir) #列出文件夹下所有的目录与文件
data_list=[]
url_list=[]
num_list=[]
split_list=['follow','subscribe','-watch exclusive','website ?','http','www','expert review','mobile no','note:','download:','..','connect with','please','ios app','découvrez-le','read detail','channel link','download link','app url','app link','buy link','about channel','click the links','click to','click on','stay tuned','news tak','Подпишитесь на','ﺎﺸﺗﺮﻛ ﻒﻳ','swagat mere channel','guys iss','like me','check out','enjoy and stay','like, share','like, and share','thanks for','thanks you for','thanx for','thanx 4','previous videos','◄','✔','❖','•','☞','☛','like us','you can also','hope you','hope u','aaj tak','know more','youtube:','remix king','read more','to watch','watch latest','for all','find latest','for latest','for more','for buy link','free signup','sign-up','click here','more info']
for i in range(len(list_file)):
    path = os.path.join(rootdir,list_file[i])
    if os.path.isfile(path):
       f= open(path,'r',encoding='utf8')
       for line in f:
           line=line.strip('\n')
           if line:
              json1=json.loads(line)
              if json1.get('countries') and json1.get('id') and json1.get('langs') and json1.get('title') and ('in' in [w.lower() for w in json1['countries']]  or 'india' in [w.lower() for w in json1['countries']]) and ('en' in json1['langs']): 
                 if json1.get('description'):
                    line=json1['description'] 
                    line=re.sub(r"\\u20[0-9][0-9]", "", line)
                    line=line.replace('‘',"'")
                    line=line.replace('’',"'")
                    line=line.replace('‒',"-")
                    line_list=line.split(' ')
                    new_list=[]
                    for word in line_list:
                        #该字符既不是全为大写，也不是全为小写
                        if word.isupper() is False and word.islower() is False:
                           for i in range(1,len(word)):
                               if ord(word[i])>=65 and ord(word[i])<=90:
                                  break
                           if i>1 and i!=len(word)-1:
                              new_word=word[:i]+' '+word[i:]
                              new_list.append(new_word)
                           else:
                              new_list.append(word)
                        else:
                              new_list.append(word)
                    line=' '.join(new_list)
                    line=line.lower()
                    line=line.replace('you tube',"youtube")
                    line=line.replace('face book',"facebook")
                    for split in split_list:
                        if re.search(split,line):
                           line=line.split(split,1)[0]
                    line=line.replace('\"a. p. j.\"','')
                    line=line.replace('\n',' ')
                    line=line.replace('\"','')

                    if line:   
                       data_list.append(json1["title"]+' '+line)
                    else:
                       data_list.append(json1["title"])
i
                 else:
                    data_list.append(json1["title"])
                 if json1.get('source_url'):
                    url_list.append(json1['source_url'])
                 else:
                    url_list.append([])
                 num_list.append(json1['id'])
rootdir1='youtube'
list_file1 = os.listdir(rootdir1) #列出文件夹下所有的目录与文件
logger.info('youtube')                
for i in range(len(list_file1)):
    path = os.path.join(rootdir1,list_file1[i])
    if os.path.isfile(path):
       f= open(path,'r',encoding='utf8')
       for line in f:
           line=line.strip('\n')
           if line:
              json1=json.loads(line)
              if json1.get('_id') and json1.get('langs') and json1.get('title') and  'en' ==  json1['langs']:
                 if json1.get('description'):
                    line=json1['description']
                    line=re.sub(r"\\u20[0-9][0-9]", "", line)
                    line=line.replace('‘',"'")
                    line=line.replace('’',"'")
                    line=line.replace('‒',"-")
                    line_list=line.split(' ')
                    new_list=[]
                    for word in line_list:
                        #该字符既不是全为大写，也不是全为小写
                        if word.isupper() is False and word.islower() is False:
                           for i in range(1,len(word)):
                               if ord(word[i])>=65 and ord(word[i])<=90:
                                  break
                           if i>1 and i!=len(word)-1:
                              new_word=word[:i]+' '+word[i:]
                              new_list.append(new_word)
                           else:
                              new_list.append(word)
                        else:
                              new_list.append(word)
                    #只保留英文字符
                    new_list1=[]
                    for word in new_list:
                        word=word.strip(' ')
                        if re.search('^[a-zA-Z0-9]+$',word):
                          new_list1.append(word)
                    line=' '.join(new_list1)
                    line=line.lower()
                    line=line.replace('you tube',"youtube")
                    line=line.replace('face book',"facebook")
                    for split in split_list:
                        if re.search(split,line):
                           line=line.split(split,1)[0]

                    line=line.replace('\"a. p. j.\"','')
                    line=line.replace('\n',' ')
                    line=line.replace('\"','')
                    if line:   
                       data_list.append(json1["title"]+' '+line)
                    else:
                       data_list.append(json1["title"])

                 else:
                    data_list.append(json1["title"])
                 if json1.get('url'):
                    url_list.append(json1['url'])
                 else:
                    url_list.append([])
                 num_list.append(json1['_id'])
train_list=[]
final_string_list=[]
final_url_list=[]
final_num_list=[]
for i in range(len(data_list)):
    line=data_list[i]
    line=line.lower()
    line=line.rstrip(' ')
    line_list=line.split(' ')
    new_list=[]
    for word in line_list:
        word=word.strip(' ')
        if re.search('^[a-z0-9]+$',word):
           #word=stemmer.stem(word)        #提取单词词干
           new_list.append(word)
    temp_list=[w for w in new_list if w not in stopwords]
    if temp_list:
       final_string_list.append(line)
       if 30//len(temp_list)>=1:   #文本长度至少为30
          integ=30//len(temp_list)
          train_list.append((temp_list*(integ+1))[:30])
       else:
          train_list.append(temp_list)
       final_url_list.append(url_list[i])
       final_num_list.append(num_list[i])
dictionary=Dictionary(train_list)
new_dict=dictionary.token2id
corpus=[]
logger.info('hello')
logger.info("字典中共{}个词".format(len(new_dict)))

for text in train_list:
    corpus.append(dictionary.doc2bow(text))
print(len(final_url_list))
print(len(final_num_list))
print(len(final_string_list))
print(len(train_list))
dict_corpus=[dictionary,corpus,final_url_list,final_num_list,final_string_list,train_list]

with open('dict_corpus.pkl','wb') as f_dump:
     pickle.dump(dict_corpus,f_dump)
f_dump.close()
logger.info('hello2')
f_times=open('word_times.txt','a',encoding='utf8')
for i in range(len(train_list)):
    transform(i,new_dict,train_list[i],f_times)
    if i>1000:
       break
     
f_times.close()
elapsed=(time.time()-start)/60
logger.info("Time used {:>4.2f} minutes".format(elapsed))
