# -*- coding: utf-8 -*-
"""
Created on Sun june 26 19:49:24 2018

@author: Administrator
"""
import json
import re
import pickle
import os
import numpy as np
import re
from logger import get_logger
import time 
# Save params
log_file_name=os.path.basename(__file__).split('.',1)[0]+'.log'
logger = get_logger(log_file_name)
f_dict= open('dict_corpus.pkl','rb')
dict_corpus=pickle.load(f_dict)
dictionary=dict_corpus[0]
new_dict=dictionary.token2id

#读id与字符的字典
f_id= open('id_string.pkl','rb')
id_string=pickle.load(f_id)
rootdir='lda_items'
start=time.time()
#将数组转化为出现的次数
def transform1(video_id):
    array=id_string[video_id]
    num_array = {}
    for word in set(array):
        num_array[word] = array.count(word)
    string1=video_id+'\x01'
    for key in num_array:
        if key in new_dict:
           string1+=str(new_dict[key])+'\x02'+str(num_array[key])+'\x03'
    string1=string1.rstrip('\x03')
    return string1+'\x01\x02\x03'
        
def transform(video_id):
    array=id_string[video_id]
    num_array = {}
    for word in set(array):
        num_array[word] = array.count(word)
    string1=video_id+'\x01'
    for key in num_array:
        if key in new_dict:
           string1+=str(new_dict[key])+'\x02'+str(num_array[key])+'\x03'
    string1=string1.rstrip('\x03')
    return string1+'\x01\x02'
def export_items(test_list,target_file,count):
    string=transform1(test_list[0])
    for item in test_list[1:]:
        temp_string=transform(item)
        string+=temp_string
    string=string.rstrip('\x01\x02')
    target_file.write(string+'\n')
    count+=1
    return count
if __name__=='__main__':
   target_file=open('item_sims.txt','w',encoding='utf8')
   list_file = os.listdir(rootdir) #列出文件夹下所有的目录与文件
   count=0
   for i in range(len(list_file)):
       path = os.path.join(rootdir,list_file[i])
       if os.path.isfile(path):
          f= open(path,'r',encoding='utf8')
          for line in f:
              line=line.strip('\n')
              if line:
                 test_list=[]
                 key=line.split('\x01')[0].split('_')[0]
                 test_list.append(key)
                 items=line.split('\x01')[1].split(',')
                 for item in items:
                     item_key=item.split('_')[0]
                     test_list.append(item_key)
                 count=export_items(test_list,target_file,count)
   target_file.close()
   elapsed=(time.time()-start)/60
   logger.info("Time used:{} minutes".format(elapsed))


