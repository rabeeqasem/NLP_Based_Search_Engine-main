import json
from tokenizec import NlpTokenizer
import re
from check_search import searcher
from tokenizec import NlpTokenizer
import pandas as pd
import numpy as np 
from PyQt5 import QtWidgets
class prox:
    def get_fn(self,text1,text2,spacing):
        text1=text1.strip()
        text2=text2.strip()
        token1=NlpTokenizer().tokenizec(text1)
        token2=NlpTokenizer().tokenizec(text2)
        f1=[]
        f1_s=pd.DataFrame(data=None,columns=['docs','space'])
        for i in range(len(token1)-1):
            docs=self.finder(token1[i],token1[i+1],1)
            if len(f1)==0:
                f1.extend(docs['docs'])
            else:
                d1=set(f1)
                d2=set(docs['docs'])
                f1=list(d1.intersection(d2))
                f1_s=docs[docs['docs'].isin(f1)]
        f2=[] 
        f2_s=pd.DataFrame(data=None,columns=['docs','space'])
        for i in range(len(token2)-1):
            docs=self.finder(token2[i],token2[i+1],1)
            if len(f2)==0:
                f2.extend(docs['docs'])
            else:
                d1=set(f2)
                d2=set(docs['docs'])
                f2=list(d1.intersection(d2)) 
                f2_s=docs[docs['docs'].isin(f2)]
        f3=[]
        f3_s=pd.DataFrame(data=None,columns=['docs','space'])
        docs=self.finder(token1[-1],token2[0],spacing)
        f3=docs['docs']
        f3_s=docs[docs['docs'].isin(f3)]
        freq=pd.DataFrame(data=None,columns=['docs','space'])
        if len(token1)>1 and len(token2)>1:
            d1=set(f1)
            d2=set(f2)
            d3=set(f3)
            f4=list(d1.intersection(d2,d3))
            freq=freq.append(f1_s,ignore_index=True)
            freq=freq.append([f2_s,f3_s],ignore_index=True)
            freq=freq[freq['docs'].isin(f4)]
            freq=freq.groupby('docs').max('space').reset_index().sort_values('space',ascending=False)
            
        elif len(token1)==1 and len(token2)>1:
            d2=set(f2)
            d3=set(f3)
            f4=list(d2.intersection(d3))
            freq=freq.append(f2_s,ignore_index=True)
            freq=freq.append(f3_s,ignore_index=True)
            freq=freq[freq['docs'].isin(f4)]
            freq=freq.groupby('docs').max('space').reset_index().sort_values('space',ascending=False)
            
        elif len(token1)>1 and len(token2)==1:
            d1=set(f1)
            d3=set(f3)
            f4=list(d1.intersection(d3))
            freq=freq.append(f1_s,ignore_index=True)
            freq=freq.append(f3_s,ignore_index=True)
            freq=freq[freq['docs'].isin(f4)]
            freq=freq.groupby('docs').max('space').reset_index().sort_values('space',ascending=False)

        elif len(token1)==1 and len(token2)==1:
            f4=f3
            freq=freq.append(f3_s,ignore_index=True)
            freq=freq[freq['docs'].isin(f4)]
            freq=freq.groupby('docs').max('space').reset_index().sort_values('space',ascending=False)
            
        return f4,freq.reset_index()
    def finder(self,token1, token2,spacing):   
        file_list=[] 
        spaces=[]
        for fn in self.data.keys():
            for tags in self.zones:
                values=self.data[fn][tags]
                if token1 in values and token2 in values:
                    for key in self.file_map.keys():
                        if fn ==self.file_map[key]:
                            k=key
                            break
                    idx1=self.pos_index[token1][1][k][tags]
                    idx2=self.pos_index[token2][1][k][tags]
                    for i in idx1:
                        for j in idx2:
                            if j-i <= spacing and j-i > 0:
                                file_list.append(fn)
                                spaces.append(j-i)
        result=pd.DataFrame(zip(file_list,spaces),columns=['docs','space'])
        result=result.groupby(by='docs').max('space').reset_index()
        return result
    
    
    def proximity(self,query,flags, zones=None):
        
        if zones==None:
            self.zones=['TITLE','LOCATION','DESCRIPTION','NOTES']
        else: self.zones=zones

        stem_with_stop={'No Stemming': "tokenized.json", 'Porter Stemmer': 'ps_stemmed.json','Snowball Stemmer':'sb_stemmed.json',
           'Lancaster Stemmer':'lc_stemmed.json','Customized Stemmer':'custom_stemmed.json'}
        self.data = json.loads(open('stemmers/'+stem_with_stop[flags['stemmer'][0]]).read())
        self.pos_index=json.loads(open('pos_index/'+'pos_'+stem_with_stop[flags['stemmer'][0]]).read())
        self.file_map=json.loads(open('pos_index/'+'file_map.json').read())
        
        query_tokens = re.findall('(/[0-9][0-9]*)',query,re.IGNORECASE)
        if len(query_tokens):
            if query.index(query_tokens[0])==0:
                query=query[query.index(query_tokens[0])+len(query_tokens[0]):]
                query_tokens = re.findall('(/[0-9])',query,re.IGNORECASE)
        if len(query_tokens):   
            if query[-len(query_tokens[-1]):]==query_tokens[-1]:
                query=query[:-len(query_tokens[-1])]
                query_tokens = re.findall('(/[0-9])',query,re.IGNORECASE)
        if len(query_tokens):    
            if flags['stemmer'][0] == 'Porter Stemmer':        
                query_tokens=searcher().Porter_Stemmer(query_tokens)
            elif flags['stemmer'][0] == 'Snowball Stemmer':        
                query_tokens=searcher().Snowball_Stemmer(query_tokens)
            elif flags['stemmer'][0] == 'Lancaster Stemmer':
                query_tokens=searcher().Lancaster_Stemmer(query_tokens)
            elif flags['stemmer'][0] == 'Customized Stemmer':
                query_tokens=searcher().Customized_Stemmer(query_tokens)   
            
            indexes=[]
            s_index=0
            for tk in query_tokens:
                index=query.index(tk,s_index)
                indexes.append(index)
                s_index+=index+len(tk)
            doc_list=[]  
            freqs=[]
            if len(query_tokens)==1:
                temp = query[:query.index(query_tokens[0])]
                temp2 = query[ query.index(query_tokens[0])+len(query_tokens[0])+1:]
                number=int(query_tokens[0].replace('/',''))
                fn, freq=self.get_fn(temp,temp2,number)
                if len(fn):
                    doc_list.append(fn)
                    freqs.append(freq)
            
            else:
                for i in range(len(query_tokens)):
                    if i==0 :
                        temp = query[:indexes[i]].strip()
                        temp2 = query[indexes[i]+len(query_tokens[i]):indexes[i+1]].strip()
                        number=int(query_tokens[i].replace('/',''))
                        fn,freq=self.get_fn(temp,temp2,number)
                        if len(fn):
                            doc_list.append(fn)
                            freqs.append(freq)
            
                    elif i==len(query_tokens)-1:
                        temp = query[indexes[i-1]+len(query_tokens[i-1]): indexes[i]].strip()
                        temp2= query[indexes[i]+len(query_tokens[i]):].strip()
                        number=int(query_tokens[i].replace('/',''))
                        fn,freq=self.get_fn(temp,temp2,number)
                        if len(fn):
                            doc_list.append(fn)
                            freqs.append(freq)
            
                    else:
                        temp = query[indexes[i-1]+len(query_tokens[i-1]):indexes[i]].strip()
                        temp2 = query[indexes[i]+len(query_tokens[i]):indexes[i+1]].strip()
                        number=int(query_tokens[i].replace('/',''))
                        fn,freq=self.get_fn(temp,temp2,number)
                        if len(fn):
                            doc_list.append(fn)
                            freqs.append(freq)
            
            docs=[]
            for l in doc_list:
                if len(docs)==0:
                    docs.extend(l)
                else:
                    f1=set(docs)
                    f2=set(l)
                    docs=list(f1.intersection(f2))
            freq=freq.groupby('docs').max('space').reset_index().sort_values('space',ascending=False)
            freq=freq[freq['docs'].isin(docs)].reset_index()
            org_files=json.loads(open('dataset.json').read())
            result={}
            for key in docs:
                result[key]=org_files[key]
        else: 
            msg= QtWidgets.QMessageBox()
            msg.setWindowTitle('Notification')
            msg.setText('Syntax Error.\n Make sure the syntax is:\nText1 /K / Text2')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            x=msg.exec_()
            result={}
        return result, freq
    
# flags=pd.DataFrame(data=np.zeros([1,11]),columns=['boolean','zone_based','cosine','wildcard','stemmer','stemming','proximity','semantic','exact_match','regex','stop_words'])
# flags['stemmer'][0]='No Stemming'
# qr='boy /5 presents'
# x,y=prox().proximity(qr,flags,zones=['TITLE'])
