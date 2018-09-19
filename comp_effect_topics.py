from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import multiprocessing
import pickle
import os
import json
import re
import time
import math
import numpy as np

start=time.clock()
f_dict= open('dict_corpus.pkl','rb')
dict_corpus=pickle.load(f_dict)
dictionary=dict_corpus[0]
corpus=dict_corpus[1]

def func(num_topic):
    temp_result=[]
    temp_result.append(num_topic)
    model=LdaModel(corpus=corpus,id2word=dictionary,num_topics=num_topic,iterations=100)
    model.save('./model/lda_'+str(num_topic)+'.model')  #保存模型
    temp_result.append(model.show_topics(num_topics=10, num_words=10))
    return temp_result

def cal_coherence(rootdir):
    rootdir = 'model'
    list_file = os.listdir(rootdir) #列出文件夹下所有的目录与文件d
    data_list=[]
    f_dict= open('dict_corpus.pkl','rb')
    coherence_list=[]
    for i in range(len(list_file)):
        path = os.path.join(rootdir,list_file[i])
        if os.path.isfile(path) and path.endswith('.model'):
           temp_name=path.split('lda_',1)[1]   #取后一部分
           num_topic=int(temp_name.split('.model',1)[0])  #取前一部分           
           lda_model = LdaModel.load(path)
           cv = CoherenceModel(model=lda_model, texts=train_list, dictionary=dictionary, coherence='c_v')
           coherence=cv.get_coherence()
           coherence_list.append([num_topic,coherence])
           #print(coherence_list)
    f=open('coherence_topic.pkl','wb')
    pickle.dump(coherence_list,f)
def cal_similarity(rootdir):
    rootdir = 'model'
    list_file = os.listdir(rootdir) #列出文件夹下所有的目录与文件d
    new_dict=dictionary.token2id
    #print(new_dict)
    length=len(new_dict)
    data_list=[]
    similarity_list=[]
    for m in range(len(list_file)):
        path = os.path.join(rootdir,list_file[m])
        if os.path.isfile(path) and path.endswith('.model'):
           temp_name=path.split('lda_',1)[1]   #取后一部分
           num_topic=int(temp_name.split('.model',1)[0])  #取前一部分           
           lda_model = LdaModel.load(path)
           topic_list=lda_model.print_topics(num_topics=-1, num_words=20)
           word_array=np.zeros([num_topic,length])
           for p in range(num_topic):
               topic = topic_list[p]
               word_list=topic[1].split('+')
               string_list=[]
               for word in word_list:
                   word=word.strip(' ')
                   temp_list=word.split('*')
                   string_list.append([float(temp_list[0]),temp_list[1].strip('"')])
                   for item in string_list:
                       if item[1] in new_dict:
                          word_array[p][new_dict[item[1]]]=item[0]
               simi_score=0
               for i in range(num_topic-1):
                   for j in range(i+1,num_topic):
                       simi_score+=word_array[i].dot(word_array[j])/(math.sqrt(np.sum(word_array[i]**2)) * math.sqrt(np.sum(word_array[j]**2)))
               simi_score=simi_score/(num_topic*(num_topic-1))

           similarity_list.append([num_topic,simi_score])
           print(m,'hello')
    f=open('similarity_topic.pkl','wb')
    pickle.dump(similarity_list,f)

    
if __name__=='__main__':
   print('current process is', os.getpid())
   pool = multiprocessing.Pool(processes=8i)  # 创建8个进程
   #找出最适合的topic个数
   results=[]
   #for i in range(450,1000,50):
   #    results.append(pool.apply_async(func,args=(i,)))
   pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
   pool.join()   # 等待进程池中的所有进程执行完毕
   final_results=[]
   for res in results:
       final_results.append(res.get())
   #print(final_results)
   with open('lda_result.pkl','wb') as f_dump:
        pickle.dump(final_results,f_dump)
   f_dump.close()
   rootdir = 'model'
   cal_similarity(rootdir)
   end=time.clock()
   print('程序用时',end-start)
