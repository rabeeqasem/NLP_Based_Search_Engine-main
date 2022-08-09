import re
from tokenizec import NlpTokenizer
from nltk.corpus import stopwords

import pandas as pd
import numpy as np
from boolean_query import boolean
from reg_ex import regular_exp_matcher
import json
from exact_match import exact_match_fun
from collections import Counter
from semantic import semantic
from cosine import cosine_sim
from proximity import prox
from PyQt5 import QtWidgets

#data = json.loads(open("tokenized.json").read())

    
def zone_matching(text,flags):
    fields=['title','location','date','description','notes']
    zones=re.findall('\((.*?)\)',text,re.IGNORECASE)
    texts={}
    docs={}
    file_names=[]
    wilds={}
    freq=pd.DataFrame(data=None,columns=['docs,freq'])
    tk=NlpTokenizer()
    
    if len(zones)==0:
        msg= QtWidgets.QMessageBox()
        msg.setWindowTitle('Notification')
        msg.setText('Syntax Error.\nMake sure the syntax is:\n(zone) Text')
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        x=msg.exec_()
        return docs, texts, freq.reset_index()
    s_index=0
    indexes=[]
    for zone in zones:
        i=text.index(zone,s_index)
        indexes.append(i)
        s_index+=i+len(zone)
    
    for i in reversed(range(len(zones))):
        if zones[i].lower() in fields:
            if i==len(zones)-1:
                temp = text[indexes[i]+len(zones[i])+1:]
            else:
                temp=text[indexes[i]+len(zones[i])+1:indexes[i+1]-1]
            if flags['wildcard'][0] == 1:
                wilds[zones[i].upper()]=re.findall("\w*\*\w*",temp)                    
                txt=re.findall("\*?\w\w*[.|:|?|'||...|!|-|()]?\w\w*\*?",temp)            
                if zones[i].upper() in texts.keys():
                    texts[zones[i].upper()].extend([item for item in txt if item not in wilds[zones[i].upper()]])
                else:
                    texts[zones[i].upper()]=[item for item in txt if item not in wilds[zones[i].upper()]]
                for zone in wilds.keys():
                    for tk in wilds[zone]:
                        exp="\\b"+tk.replace('*','\w*')
                        files={}
                        files =regular_exp_matcher().reg_ex('Find All',exp,tags=[zone])
                        file_names.extend(list(files.keys()))
                        docs.update(files)

            elif flags['boolean'][0] == 1:    
                files=boolean().bool_match(tk.tokenizec(temp), flags,tag=zones[i].upper())
                file_names.extend(list(files.keys()))
                docs.update(files)
                        
            elif flags['exact_match'][0]==1:
                freq_exct,files=exact_match_fun(temp,flags,zone=zones[i].upper())
                file_names.extend(list(files.keys()))
                docs.update(files)
                freq.append(freq_exct,ignore_index=True)
            elif flags['semantic'][0]==1:
                files, freq_sem=semantic().semantic_search(temp,flags,zone=zones[i].upper())
                file_names.extend(list(files.keys()))
                docs.update(files)
                freq.append(freq_sem,ignore_index=True)
            elif flags['cosine'][0] ==1:
                docs=cosine_sim().cosine(flags,temp,zones=[zones[i].upper()]) 
            elif flags['proximity'][0] ==1:
                docs,freq_prox=prox().proximity(temp,flags,zones=[zones[i].upper()])
                freq.append(freq_prox,ignore_index=True)

            else:
                texts[zones[i].upper()]=tk.tokenizec(temp)        
            
            if flags['stop_words'][0] == 1:   
                Stopwords=stopwords.words('english')
                for key in texts.keys():
                    tokens=[]
                    for token in texts[key]:
                        if token not in Stopwords:
                            tokens.append(token)
                    texts[key]=tokens
        else:
            msg= QtWidgets.QMessageBox()
            msg.setWindowTitle('Notification')
            msg.setText('Syntax Error.\nMake sure the syntax is:\n(zone) Text')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            x=msg.exec_()
    freq_files=Counter(file_names)
    freq=freq.append(pd.DataFrame(zip(freq_files.keys(),freq_files.values()),columns=['docs','freq']).sort_values(by='freq',ascending=False))
    freq=freq.groupby(by='docs')['freq'].sum().reset_index().sort_values(by='freq',ascending=False,ignore_index=True)
    
    t2={}
    for zone in texts.keys():
        if len(texts[zone]):
            t2[zone]=texts[zone] 
    #texts=t2                           
    print(t2)
    return docs, texts, freq.reset_index()

# flags=pd.DataFrame(data=np.zeros([1,10]),columns=['boolean','zone_based','cosine','wildcard','stemming','proximity','semantic','exact_match','regex','stop_words'])
# flags['wildcard'][0]=1
# x,y,z=zone_matching('(title) bra* (title) side (description) plaza',flags)