# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 10:07:41 2021

@author: loai_
"""
import pandas as pd
import re
import json
from tqdm import tqdm

class regular_exp_matcher():
    
    def reg_ex (self, func_type,reg_ex, data=None, tags=None):
        if tags==None:
            tags=['DOCNO', 'TITLE', 'DESCRIPTION', 'NOTES', 'LOCATION', 'DATE', 'IMAGE', 'THUMBNAIL']
        if data==None:
            data = json.loads(open("dataset_lower.json").read())
        
        docs={}
        flag=0
        while flag<2:            
            if func_type=='Match' :
                for file in data.keys():
                    for tag in tags:
                        if re.match(reg_ex,str(data[file][tag]),re.IGNORECASE) is not None: 
                            docs[file]=data[file]
                            break
            elif func_type=='Search' :
                for file in data.keys():
                    for tag in tags:
                        if re.search(reg_ex,str(data[file][tag]),re.IGNORECASE) is not None: 
                            docs[file]=data[file]
                            break
            elif func_type=='Find All':
                 for file in data.keys():
                    for tag in tags:
                        if len(re.findall(reg_ex,str(data[file][tag]),re.IGNORECASE)): 
                            docs[file]=data[file]
                            break
            if len(docs)==0 and flag<1:
                data = json.loads(open("dataset.json").read())
                flag+=1
            else: flag=2
        return docs



