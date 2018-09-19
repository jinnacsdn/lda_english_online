# -*- coding: UTF-8 -*-
import numpy as np
import faiss
from faiss import normalize_L2
import os
import datetime
import boto3
import time
from logger import get_logger
dt = datetime.datetime.today() + datetime.timedelta(days=-1)
dt = dt.strftime('%Y%m%d')
SENTENCE_EMBEDDING='/data/chenzk/LDA/sims/'
FASTTEXT_SEARCH='1/{}/'.format(dt)
CANDY=100  #候选集
SIM_STEP=10000 #计算相似度的
FILE_STEP=300000 #上传到s3的大小 180k左右

def create_folder():
    if FASTTEXT_SEARCH != '':
        try:
            os.makedirs(FASTTEXT_SEARCH)
        except :
            pass

def cosine_index(training_vectors):
    '''
    cosine_similarity exact mode
    use
    :return:
    '''
    print(training_vectors.shape)
    d = training_vectors.shape[1]                           # dimension
    t1 = time.time()
    normalize_L2(training_vectors)
    index=faiss.IndexFlatIP(d)
    index.train(training_vectors)

    index.add(training_vectors)
    t2 = time.time()
    logger.info('{} times is {}'.format('add and train', t2 - t1))
    return index

def cosine_index_ivf(training_vectors):

    '''
    cosine_similarity exact mode
    use
    :return:
    '''
    print(training_vectors.shape)
    (num, d) = training_vectors.shape                      # dimension
    # nb = 100                  # database size
    # training_vectors= np.random.random((nb, d)).astype('float32')*10
    t1 = time.time()

    nlist = max(5,int(num/500))  # 聚类中心的个数
    normalize_L2(training_vectors)
    quantizer=faiss.IndexFlatIP(d)

    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
    index.train(training_vectors)
    index.nprobe =max(1,int(nlist*0.7))   # default nprobe is 1, try a few more
    index.add(training_vectors)
    t2 = time.time()
    logging.info('{} times is {}'.format('add and train', t2 - t1))

    quantizer.this.disown()
    index.own_fields = True

    return index

def cosine_search(index,start,end,training_vectors,item_id):
    t1=time.time()
    end=min(training_vectors.shape[0],end)
    print('ee')
    score, sim_id=index.search(training_vectors[start:end], CANDY)
    t2=time.time()
    logging.info('{}-{} times is {} ,len of sim id is {}'.format(start,end,t2-t1,sim_id.shape))
    sim_video_id=[]
    (si, sj) = sim_id.shape
    for i in range(si):
        i_list=[]
        for j in range(sj):
            i_list.append(item_id.get(sim_id[i][j],'')+'_'+str(score[i][j]))
        sim_video_id.append(i_list)
    files_name=write_local(sim_video_id, start)

def write_local(sim_video_id,start):
    si=len(sim_video_id)
    files_name=[]
    for i in range(0,si,FILE_STEP):
        path=FASTTEXT_SEARCH + str(start) + '_' +str(i)
        files_name.append(path)
        with open(path,'w') as f:
            for si in sim_video_id[i:i+FILE_STEP]:
                f.writelines(si[0]+'\x01'+','.join(si[1:])+'\n')
    return files_name

def read_local():
    local_path=[]
    for root, dirs, files in os.walk(SENTENCE_EMBEDDING):
        for file in files:
            local_path.append(os.path.join(root, file))

    item_id={}
    sentence_embedding=[]
    count=0
    for l in local_path:
        with open(l,'r') as f:
            lines=f.readlines()
        for line in lines:
            line=line.strip()
            try:
                if 'v'  in line.split('\x01')[0]:
                    sentence_embedding.append(line.split('\x01')[1].split(','))
                    item_id[count]=line.split('\x01')[0]
                    count+=1
            except:
                print(line)


    senten_npa=np.array(sentence_embedding, dtype=np.float32)
    return item_id,senten_npa

def fasttext_embedding_sim():
    t1=time.time()
    create_folder()
    item_id, sentence_embedding=read_local()
    t2=time.time()
    lines=sentence_embedding.shape[0]
    logging.info('{} times is {}'.format('read data', t2 - t1))
    # index=cosine_index(sentence_embedding) #精确模式
    index =cosine_index_ivf(sentence_embedding) #倒排模式
    t1=time.time()
    for start in range(0,lines,SIM_STEP):
            cosine_search(index, start, start+SIM_STEP, sentence_embedding, item_id)
    t2 = time.time()
    logger.info(' total cost {} '.format(t2-t1))

fasttext_embedding_sim()
