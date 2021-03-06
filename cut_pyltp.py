# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 19:25:21 2018

@author: xhlgogo
"""

import os
import re
from pyltp import Segmentor
from pyltp import Postagger
#from tqdm import tqdm
import threading


def children(forder_list):
    
    LTP_DATA_DIR = 'E:/Program Files/workspace/ltp_data_v3.4.0'  # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    
    read_path = "E:/Program Files/workspace/report/"
    write_sen_path = "E:/Program Files/workspace/report_sentence/"
    write_word_path = "E:/Program Files/workspace/report_word/"
    
# =============================================================================
#     for forder in tqdm(forder_list, desc='%s loop'%threading.current_thread().name):
#         sleep(0.1)
# =============================================================================
    for forder in forder_list:
        print("thread "+threading.current_thread().name+" is doing "+forder)
        file_list = os.listdir(read_path+forder)
        for file_name in file_list:
            if file_name=="desktop.txt":
                os.remove(read_path+forder+'/'+file_name)
                continue
            elif file_name=="desktop.ini":
                continue
            with open(read_path+forder+'/'+file_name,'r',encoding="utf-8") as file:
                content = file.readlines()
            
            #去除首尾两行
            if "政府工作报告" in content[1]:
                content.pop(0)
                content.pop(0)
            if "来源" in content[-2]:
                content.pop()
                content.pop()
                
            #去除原文中的非中文字符,分句
            content_have_num = []  #含数字的分句
            content_not_num = []   #不含数字的分句
            for element in content:
                #将中英文双引号、顿号去掉
                temp1_element = re.sub(r'[\、\”\“\"]', '',element)
                #将数字替换为“数”
                temp2_element = re.sub(r'[0-9]+\.?[0-9]+|[\d]','数',temp1_element)
                #将非中文字符用空白替换
                new_element = re.sub(r'[^\u4e00-\u9fa5]', ' ', temp2_element).split(' ')
                for item in new_element:
                    #过滤去除字符后只剩一个字的元素
                    if len(item) >= 2 and len(item) < 4:
                        if "数" not in item:
                            content_have_num.append(item.strip())
                    elif len(item) >= 4:
                        content_have_num.append(item.strip())
                        if "数" not in item:
                            content_not_num.append(item.strip())
                            
            #分别写含数字和不含数字的分句文件
            with open(write_sen_path+forder+'/have_num_'+file_name,'w',encoding="utf-8") as file:
                file.write('\n'.join(content_have_num))  
            with open(write_sen_path+forder+'/not_num_'+file_name,'w',encoding="utf-8") as file:
                file.write('\n'.join(content_not_num))
                
            #对不含数字的句子分词
            words_postags = []
            for element in content_not_num:
                words = list(segmentor.segment(element))
                postags = list(postagger.postag(words))
                words_postags.append(' '.join(words))
                words_postags.append(' '.join(postags))
            
            #写不含数字的句子的分词和词性
            with open(write_word_path+forder+'/'+file_name,'w',encoding="utf-8") as file:
                file.write('\n'.join(words_postags)) 
    
              
    postagger.release()  # 释放模型
    segmentor.release()  # 释放模型


if __name__=="__main__":

    forder_list1 = ["北京市","天津市","上海市","河北省","山西省","辽宁省","吉林省","重庆市"]
    forder_list2 = ["黑龙江","江苏省","浙江省","安徽省","福建省","江西省","山东省","河南省"]
    forder_list3 = ["湖北省","湖南省","广东省","海南省","四川省","贵州省","云南省","陕西省"]
    forder_list4 = ["中央","甘肃省","青海省","内蒙古","广西省","西藏省","宁夏省","新疆省"]
    
    print("thread %s is runing......"%threading.current_thread().name)
    t1 = threading.Thread(target=children, args=(forder_list1,), name="List1")
    t2 = threading.Thread(target=children, args=(forder_list2,), name="List2")
    t3 = threading.Thread(target=children, args=(forder_list3,), name="List3")
    t4 = threading.Thread(target=children, args=(forder_list4,), name="List4")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print("thread %s is end."%threading.current_thread().name)