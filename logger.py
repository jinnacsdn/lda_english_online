# -*- coding: utf-8 -*-i
"""
Created on Sun june 26 19:49:24 2018

@author: Administrator
"""

import logging
def get_logger(log_file,mode='w'):
    file_h = logging.FileHandler(log_file,mode=mode, encoding='utf8')
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.DEBUG)
    #����һ����ʽ��������ӵ�ָ����handlers
    file_h = logging.FileHandler(log_file)
    #ָ��д���ļ�����ͷַ�log��Ϣ�ļ�������loggingģ��ֻ�����DEBUG�����ϵ�log
    file_h.setLevel(logging.DEBUG)
    stream_h = logging.StreamHandler()
    #ָ���������Ļ����ͷַ�log��Ϣ�ļ�������loggingģ��ֻ�����INFO�����ϵ�log
    stream_h.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_h.setFormatter(formatter)
    file_h.setFormatter(formatter)
    logger.addHandler(stream_h)
    logger.addHandler(file_h)
    return logger

