"""
Created on Sun Feb  7 23:34:26 2021

@author: loai_
"""
import re
import json
from reg_ex import regular_exp_matcher
from tokenizec import NlpTokenizer
from matcher import matcher
from collections import Counter
from nltk.corpus import stopwords
from check_search import searcher
import pandas as pd
import numpy as np
data = json.loads(open("dataset_lower.json").read())

def exact_match_fun(query,flags,zone=None):
    docs={}
    tk = NlpTokenizer()
    x = (re.findall(r'"(.*?)"', query.lower()))
    input_match = x[0]
    input_token = tk.tokenizec(input_match)
    tokenized = tk.tokenizec(query.lower())
    tokens = [item for item in tokenized if item not in input_token]
    final_tokens=[]
    if flags['stop_words'][0] == 1:   
        Stopwords=stopwords.words('english')
        for t in tokens:
            if t not in Stopwords:
                final_tokens.append(t)
    if flags['stemmer'][0] == 'Porter Stemmer':        
        final_tokens=searcher().Porter_Stemmer(final_tokens)
    elif flags['stemmer'][0] == 'Snowball Stemmer':        
        final_tokens=searcher().Snowball_Stemmer(final_tokens)
    elif flags['stemmer'][0] == 'Lancaster Stemmer':
        final_tokens=searcher().Lancaster_Stemmer(final_tokens)
    elif flags['stemmer'][0] == 'Customized Stemmer':
        final_tokens=searcher().Customized_Stemmer(final_tokens)
    
    if zone != None:
        files_exact =regular_exp_matcher().reg_ex('Find All',input_match,tags=[zone.upper()])
        freq_t, files_tokens= matcher(final_tokens,flags,tags=[zone.upper()])
        docs.update(files_exact)
        docs.update(files_tokens)
        
    else:
        files_exact =regular_exp_matcher().reg_ex('Find All',input_match)
        freq_t, files_tokens= matcher(final_tokens,flags)
        docs.update(files_exact)
        docs.update(files_tokens)
    
    f1=list(files_exact.keys())
    freq=Counter(f1)
    freq=pd.DataFrame(zip(freq.keys(),freq.values()),columns=['docs','freq']).sort_values(by='freq',ascending=False,ignore_index=True)
    freq=freq.append(freq_t,ignore_index=True)
    freq=freq.groupby(by='docs')['freq'].sum().reset_index().sort_values(by='freq',ascending=False,ignore_index=True)
    return freq, docs


# query = 'plaza armas "plaza" de'

# flags=pd.DataFrame(data=np.zeros([1,11]),columns=['boolean','zone_based','cosine','wildcard','stemmer','stemming','proximity','semantic','exact_match','regex','stop_words'])
# flags['stemmer'][0]='Porter Stemmer'
# flags['stop_words'][0]=1       
# x1,x2=exact_match_fun(query,flags)

