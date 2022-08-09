from tokenizec import NlpTokenizer
from nltk.corpus import wordnet as wn
import pandas as pd
from tqdm import tqdm
import numpy as np
from nltk.corpus import stopwords
from check_search import searcher
from matcher import matcher
from boolean_query import boolean
from collections import Counter
import json
import re
class semantic:

    #this is the function you need to call in the GUI
    #it recives a flag and it transfare you you to the wonted semantic method
    def semantic_search(self,text,flags,zone=None):
        if flags['ontology'][0]=='Word Net':
            print('wordnet')
            docs, freq=self.wordnet(text, flags,zone)
            #wordnet
        elif flags['ontology'][0]=='Yago5':
            print('yago')
            docs, freq=self.yago(text,flags,zone)
            #Yago5
        return docs, freq

    def generate_ngrams(self,s, n):
        # Convert to lowercases
        s = s.lower()
    
        # Replace all none alphanumeric characters with spaces
        s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    
        # Break sentence in the token, remove empty tokens
        tokens = [token for token in s.split(" ") if token != ""]
    
        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]
        # wn.synsets('Auto')----> [Synset('car.n.01')]
        #wn.synsets('Auto).lemmas()------>[Lemma('car.n.01.car'),
        #  Lemma('car.n.01.auto'), Lemma('car.n.01.automobile'), Lemma('car.n.01.machine'), Lemma('car.n.01.motorcar')]

    def wordnet(self,text, flags,zone):
        tc=NlpTokenizer()
        tkn=tc.unitoknizer(text)
        sem=[]
        # when we receive a twogram token or more it will search for each word and return a list
        for tk in tkn:
            token=wn.synsets(tk)
            sem.append(tk)
            for tkk in range(len(token)):
                for index in range(len(token[tkk].lemmas())):
                    sem.append(token[tkk].lemmas()[index].name().lower())
        sem=list(set(sem))
        if flags['stop_words'][0]==1:
            Stopwords=stopwords.words('english')
            sem=[item for item in sem if item not in Stopwords]
        if flags['stemmer'][0] == 'Porter Stemmer':        
            sem=searcher().Porter_Stemmer(sem)
        elif flags['stemmer'][0] == 'Snowball Stemmer':        
            sem=searcher().Snowball_Stemmer(sem)
        elif flags['stemmer'][0] == 'Lancaster Stemmer':
            sem=searcher().Lancaster_Stemmer(sem)
        elif flags['stemmer'][0] == 'Customized Stemmer':
            sem=searcher().Customized_Stemmer(sem)

        if zone == None:
            freq,docs=matcher(sem, flags)
            
        elif zone != None: 
            freq,docs=matcher(sem, flags, tags=[zone.upper()])
        
        return docs, freq

    def yago(self,text, flags, zone=None):
        print('yago')
        results = []
        ln = len(text.split())
        for x in range(ln):
            result = self.generate_ngrams(text,ln- x)
            results.append(result)

        token=results
        yago=[text]
        for tk in tqdm(token):
            for t in tqdm(tk):
                y=self.doyago(t)
                yago.extend(y)
        
        file_names=[]
        docs={}
        if zone == None:
            freq, docs=matcher(yago, flags)
            return docs, freq
        elif zone != None: 
            freq, docs=matcher(yago,flags,tags=[zone.upper()])
            return docs, freq


    def doyago(self,text):
        newtext='<'+text.replace(' ','_')+'>'
        newtext=newtext.strip()
        newtext=newtext.lower()
        path='yago_df.csv'

        df=pd.read_csv(path)
        data=df['subject']==newtext
        data2=df[data]
        sem_list=list(data2['object'])
        yago_sem=[]
        #yago_sem=[text]
        for lt in range(len(sem_list)):
            text=sem_list[lt].replace('_',' ')
            text=text.replace('<','')
            text=text.replace('>','')
            text=text.replace('-','')
            text=text.strip()
            yago_sem.append(text)
        return yago_sem
            

        
######

# se=semantic()
# print(se.wordnet('bike'))
# print(se.yago('cristiano ronaldo'))

# flags=pd.DataFrame(data=np.zeros([1,12]),columns=['boolean','zone_based','cosine','wildcard','stemming','stemmer','proximity','semantic','ontology','exact_match','regex','stop_words'])
# flags['ontology'][0]='Word Net'

