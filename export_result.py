# -*- coding: utf-8 -*-
"""
Created on Sun june 26 19:49:24 2018

@author: Administrator
"""
import json
import re
import pickle
import os
import math
from logger import get_logger
import re
import time
import boto3
from sklearn.metrics.pairwise import cosine_similarity
import datetime
now_time = datetime.datetime.now().strftime('%Y%m%d')   #�����ʱ�䲢ת��Ϊ�ַ���
BUCKET_NAME="recommendation.ap-southeast-1"
s3 = boto3.resource('s3') 
BUCKET_PREFIX_NLP="short_video_nlp/"
BUCKET_PREFIX_LABEL="{}short_video_LDA/".format(BUCKET_PREFIX_NLP)
currentdir=os.getcwd()
log_file_name=os.path.basename(__file__).split('.',1)[0]+'.log'
# Save params
#����־�ļ���СС��1kʱ������׷��ģʽд 
if os.path.exists(log_file_name) is False or os.path.getsize(log_file_name)/1024<1:
   logger = get_logger(log_file_name,mode='a')
else:
   #����ɾ����ǰ����־ 
   logger = get_logger(log_file_name)

#��id���ַ����ֵ�
f_id= open('id_string.pkl','rb')
id_string=pickle.load(f_id)
rootdir='lda_items'

def upload_s3(local_file_full_path,datepart = now_time):
    #'''
    #:param local_file_full_path: ��Ҫ�ϴ��ļ���������ַ
    #:param datepart: ����ϴ����ĸ�����Ŀ¼��
    #:return:
    #'''
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(BUCKET_NAME)
    logger.info('this is upload  id_label_,labelling_system')
    file_name=os.path.split(local_file_full_path)[1]
    s3_path= BUCKET_PREFIX_LABEL + 'datepart={}/'.format(datepart)
    logger.info('upload  lda to {}'.format(s3_path))
    mybucket.upload_file(local_file_full_path, s3_path + file_name)

#������ת��Ϊ���ֵĴ���
def transform(array):
    num_array = {}
    for word in set(array):
        num_array[word] = array.count(word)
    return num_array
def export_result(test_list,count):   
    if len(str(count))==1:
       target_file='00000'+str(count)+'_0'
    elif len(str(count))==2:
       target_file='0000'+str(count)+'_0'
    elif len(str(count))==3:
       target_file='000'+str(count)+'_0'
    elif len(str(count))==4:
       target_file='00'+str(count)+'_0'
    f=open(target_file,'a',encoding='utf8')
    complete_string=test_list[0]+'\x01'
    init_den=0
    init_dict=transform(id_string[test_list[0]])
    for key in init_dict:
        init_den+=init_dict[key]**2
    init_den=math.sqrt(init_den)
    temp_string=''
    for item in test_list[1:]: 
        comp_dict=transform(id_string[item])
        temp_dict={}  #���ڱ��������ֵ�Ĺ�ͬԪ��
        for key in init_dict:
            if key in comp_dict:
               temp_dict[key]=[init_dict[key],comp_dict[key]]
        comp_den=0
        for key in comp_dict:
            comp_den+=comp_dict[key]**2
        comp_den=math.sqrt(comp_den)
        numerator=0
        if len(temp_dict)>0:
           for key in temp_dict:
               numerator+=temp_dict[key][0]*temp_dict[key][1]
           cos_val=numerator/(init_den*comp_den)  #�����������ƶ�
           if cos_val>0.25:
              temp_string+=item+','
    if len(temp_string)>0:
       complete_string+=temp_string.rstrip(',')
       f.write(complete_string+'\n')
    #����ļ��Ĵ�С����1M����д����һ���ļ���
    if os.path.getsize(target_file)/1024/1024>=1:
       local_path=os.path.join(currentdir,target_file)
       upload_s3(local_path)
       logger.info("file:{}".format(count))
       count+=1
       f.close()
    return count
if __name__=='__main__':
   start=time.time()
   list_file = os.listdir(rootdir) #�г��ļ��������е�Ŀ¼���ļ�
   count=0
   for i in range(len(list_file)):
       path = os.path.join(rootdir,list_file[i])
       if os.path.isfile(path):
          f= open(path,'r',encoding='utf8')
          try:
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
                 count=export_result(test_list,count)
          except Exception as e:
               print(path)
               print(e)
               print(line)
   elapsed=(time.time()-start)/60
   logger.info("Time used:{} minutes".format(elapsed))

