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
    #创建一个格式并把它添加到指定的handlers
    file_h = logging.FileHandler(log_file)
    #指定写入文件的最低分发log信息的级别，这里logging模块只会输出DEBUG及以上的log
    file_h.setLevel(logging.DEBUG)
    stream_h = logging.StreamHandler()
    #指定输出到屏幕的最低分发log信息的级别，这里logging模块只会输出INFO及以上的log
    stream_h.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_h.setFormatter(formatter)
    file_h.setFormatter(formatter)
    logger.addHandler(stream_h)
    logger.addHandler(file_h)
    return logger

