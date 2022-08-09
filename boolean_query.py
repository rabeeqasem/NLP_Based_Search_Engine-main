from nltk.corpus import stopwords

import numpy as np
import json

import pandas as pd
from PyQt5 import QtWidgets




class boolean ():
    def loader(self,flags):
        stem_no_stop={'No Stemming': "without_stopword_tokenized.json", 'Porter Stemmer': 'without_stopword_ps_stemmed.json','Snowball Stemmer':'without_stopword_sb_stemmed.json',
           'Lancaster Stemmer':'without_stopword_lc_stemmed.json','Customized Stemmer':'without_stopword_custom_stemmed.json'}

        stem_with_stop={'No Stemming': "tokenized.json", 'Porter Stemmer': 'ps_stemmed.json','Snowball Stemmer':'sb_stemmed.json',
           'Lancaster Stemmer':'lc_stemmed.json','Customized Stemmer':'custom_stemmed.json'}
        if flags['stop_words'][0] == True:
            self.data = json.loads(open('stemmers/'+stem_no_stop[flags['stemmer'][0]]).read())
            self.pos_index=json.loads(open('pos_index/'+'pos_'+stem_no_stop[flags['stemmer'][0]]).read())
        elif flags['stop_words'][0] == False:
            self.data = json.loads(open('stemmers/'+stem_with_stop[flags['stemmer'][0]]).read())
            self.pos_index=json.loads(open('pos_index/'+'pos_'+stem_with_stop[flags['stemmer'][0]]).read())
        self.file_map=json.loads(open('pos_index/'+'file_map.json').read())
    
    def bool_match(self,text,flags,tag=None):
        self.loader(flags)
        
        operator_words = []
        cnt = 1
        query_words = []
        not_found=[]
        for i,word in enumerate(text):
            if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
                query_words.append(word.lower())
                if len(operator_words) != len(query_words)-1:
                    operator_words.append("and")
            else:
                if text[i+1].lower()=='not' or text[i+1]==text[i] or text[i+1] in ['and','or','not']:
                    pass
                else:
                    operator_words.append(word.lower())
                    
        if len(query_words)==1:
            operator_words.append('and')

        print(len(query_words))
        print(len(operator_words))
        
        total_files = len(self.file_map) ## need to stor as file
        one_hot_vector = []
        one_hot_vector_of_all_words = []
        for word in (query_words):
            if word.lower() in set(self.pos_index.keys()):
                one_hot_vector = [0] * total_files
                
                if tag != None:
                    foundlist=[]
                    for file in self.pos_index[word][1].keys():
                        if tag in self.pos_index[word][1][file].keys():
                            foundlist.append(file)
                else:
                    foundlist = list(self.pos_index[word][1].keys())
                    
                for i,doc in enumerate(foundlist):
                    one_hot_vector[int(doc)] = 1
                    
                
               
                one_hot_vector_of_all_words.append(one_hot_vector)
                
            else:
                not_found.append(word)
                vector = [0] * total_files
                one_hot_vector_of_all_words.append(vector)
                print(word,' not found')
                
        if len(query_words)==1:
                vector = [1] * total_files
                one_hot_vector_of_all_words.append(vector)
        
        
        print(len(one_hot_vector_of_all_words))
        for word in operator_words:
            copy_list1 = one_hot_vector_of_all_words[0]
            copy_list2 = one_hot_vector_of_all_words[1]
            if word == "and" :
                cells = [w1 & w2 for (w1,w2) in zip(copy_list1,copy_list2)]
                one_hot_vector_of_all_words.remove(copy_list1)
                one_hot_vector_of_all_words.remove(copy_list2)
                one_hot_vector_of_all_words.insert(0, cells)
                
            elif word == "or":
                cells = [w1 | w2 for (w1,w2) in zip(copy_list1,copy_list2)]
                one_hot_vector_of_all_words.remove(copy_list1)
                one_hot_vector_of_all_words.remove(copy_list2)
                one_hot_vector_of_all_words.insert(0, cells)
            elif word == "not":
                cells = [not w1 for w1 in copy_list2]
                cells = [int(b == True) for b in cells]
                one_hot_vector_of_all_words.remove(copy_list2)
                one_hot_vector_of_all_words.remove(copy_list1)
                cells = [w1 & w2 for (w1,w2) in zip(copy_list1,cells)]
        one_hot_vector_of_all_words.insert(0, cells)
                
        files_results = []   
        list_doc  = {}
        one_hot_list = one_hot_vector_of_all_words[0]
        cnt = 0
        for index in one_hot_list:
            if index == 1:
                files_results.append(self.file_map[str(cnt)])
                list_doc[self.file_map[str(cnt)]]= self.data[self.file_map[str(cnt)]]
            cnt = cnt+1
        
        results={}            
        data = json.loads(open("dataset.json").read())
        for file in files_results:
            results[file]=data[file]
        
        return results
  
    
# flags=pd.DataFrame(data=np.zeros([1,12]),columns=['boolean','zone_based','cosine','wildcard','stemming','stemmer','proximity','semantic','ontology','exact_match','regex','stop_words'])
# flags['stemmer']='No Stemming'
# #flags['stop_words']=1
# qr=['plaza', 'and', 'de' ,'and', 'not', 'armas']
    
# x=boolean().bool_match(qr,flags,tag='TITLE')

