# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 20:07:58 2021

@author: loai_
"""
import json
from collections import Counter
import pandas as pd
def matcher(tokens,flags,tags=None):
    data=json.loads(open('dataset.json').read())
    stem_no_stop={'No Stemming': "without_stopword_tokenized.json", 'Porter Stemmer': 'without_stopword_ps_stemmed.json','Snowball Stemmer':'without_stopword_sb_stemmed.json',
           'Lancaster Stemmer':'without_stopword_lc_stemmed.json','Customized Stemmer':'without_stopword_custom_stemmed.json'}
    
    stem_with_stop={'No Stemming': "tokenized.json", 'Porter Stemmer': 'ps_stemmed.json','Snowball Stemmer':'sb_stemmed.json',
       'Lancaster Stemmer':'lc_stemmed.json','Customized Stemmer':'custom_stemmed.json'}

    if flags['stop_words'][0] == True:
        #data = json.loads(open('stemmers/'+stem_no_stop[flags['stemmer'][0]]).read())
        pos_index=json.loads(open('pos_index/'+'pos_'+stem_no_stop[flags['stemmer'][0]]).read())
    elif flags['stop_words'][0] == False:
        #data = json.loads(open('stemmers/'+stem_with_stop[flags['stemmer'][0]]).read())
        pos_index=json.loads(open('pos_index/'+'pos_'+stem_with_stop[flags['stemmer'][0]]).read())
    file_map=json.loads(open('pos_index/'+'file_map.json').read())

    docs=[] 
    tokens=[item.strip() for item in tokens]
    for tk in tokens:
       if tk in pos_index.keys():
            if tags != None:
                 for file in pos_index[tk][1].keys():
                     for tag in tags:
                         if tag.upper() in pos_index[tk][1][file].keys():
                             docs.append(file)
                
            else: 
                docs.extend(list(pos_index[tk][1].keys()))
    files=[]
    for doc in docs:
        files.append(file_map[doc])
    freq=Counter(files)
    freq=pd.DataFrame(zip(freq.keys(),freq.values()),columns=['docs','freq']).sort_values(by='freq',ascending=False,ignore_index=True)

            # if len(docs)==0:
            #     docs=tk_docs
            # else:
            #     docs_k=set(docs)
            #     tk_k=set(tk_docs)
            #     match=docs_k.intersection(tk_k)
            #     docs=[key for key in match]
    files={}
    for key in docs:
        files[file_map[key]]=data[file_map[key]]
    
    return freq, files

# import pandas as pd
# import numpy as np
# flags=pd.DataFrame(data=np.zeros([1,11]),columns=['boolean','zone_based','cosine','wildcard','stemmer','stemming','proximity','semantic','exact_match','regex','stop_words'])
# flags['stemmer'][0]='No Stemming'
# flags['stop_words'][0]=1       
# x=matcher(['plaza','hotel'],flags,'title')
                
    
        