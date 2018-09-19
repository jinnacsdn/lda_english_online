
from collections import defaultdict
import random
import smart_open
import os
import boto3
import datetime
import json
import logging
import json
import re
from collections import defaultdict
from googletrans import Translator

from sqlalchemy import create_engine, MetaData, Table
import random

#label 系統的使用和結果的上傳label_pred/labelling_system_2.py

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
BUCKET_NAME="recommendation.ap-southeast-1"
BUCKET_PREFIX_INFO="short_video_nlp/short_video_label/labelling_system/"
LOCAL_INFO='/data/labelling_system/info/'

s3 = boto3.resource('s3')
translator = Translator(service_urls=['translate.google.cn'])
# 'recommendation.ap-southeast-1/short_video_nlp/short_video_label/'
PROD_TYPE='prod' #dev #prod
TOTAL_NUMS=3000
LOCAL_REDIS='/data/labelling_system/redis/'
BUCKET_PREFIX_LABEL="short_video_nlp/short_video_label/"
# nlb-ushareit-rcmd-tensorflow-dev-9f6803b4d6676356.elb.ap-southeast-1.amazonaws.com
engine = create_engine('postgresql://postgres:admin@127.0.0.1/postgres',
                       client_encoding='utf8')

dt = datetime.datetime.today() + datetime.timedelta(days=-1)
dt = dt.strftime('%Y%m%d')


def download_file(dt):
    logging.info('step1 this is download from s3')
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(BUCKET_NAME)
    bucket_prefix = BUCKET_PREFIX_INFO+'{}'.format(dt)

    logging.info(bucket_prefix)
    objs = mybucket.objects.filter(
        Prefix=bucket_prefix)
    filename_list = []
    for obj in objs:

        path, filename = os.path.split(obj.key)

        # if '_0' not in filename:
        #     continue
        # print(filename)
        filename_list.append(filename)
        local_path = LOCAL_INFO+'{}/'.format(dt)

        try:
            os.makedirs(local_path)

        except FileExistsError:
            pass


        mybucket.download_file(obj.key, local_path + filename)
    logging.info('{}  files  has been downloaded  from {}'.format(len(filename_list),bucket_prefix))
    return filename_list

def prepare_labelling():
    filename_list=download_file(dt)
    if len(filename_list)>0:
        upload_redis(dt)


def upload_redis(dt=''):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(BUCKET_NAME)
    if dt=='':
        dt='20180528'

    logging.info('step8/4 this is upload  label_bucket,all_label concerned to label to /video_label/detepart')
    label_bucket=[]
    all_label=[]
    label_count=''


    local_redis_path=LOCAL_REDIS+dt+'/'
    for root, dirs, files in os.walk(local_redis_path):
        for file in files:
            if 'label_system_' in file:
                all_label.append(file.split('/')[-1])

    id_label_prefix = BUCKET_PREFIX_LABEL + 'redis/id_label_{}/datepart={}/'.format(PROD_TYPE,dt)
    logging.info('upload  id_label_prefix to {}'.format(id_label_prefix))
    logging.info('files in all_label {}'.format(all_label))

    for l in all_label:
        mybucket.upload_file(local_redis_path + l, id_label_prefix + l)

import sys
a = sys.argv[1]


if a=='prepare':
    num = sys.argv[2]
    TOTAL_NUMS = int(num)
    prepare_labelling() #morning 9am
else:
    labelling_result() # 9 pm



