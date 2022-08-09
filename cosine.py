from nltk.corpus import stopwords
from collections import Counter
from tokenizec import NlpTokenizer
from tqdm import tqdm
import numpy as np
import math
import json
from check_search import searcher
import pandas as pd
class cosine_sim:

    def doc_freq(self,word):
        c = 0
        try:
            c = self.DF[word]
        except:
            pass
        return c

    def cosine(self,flags,query, zones=None):
        stem_no_stop={'No Stemming': "without_stopword_tokenized.json", 'Porter Stemmer': 'without_stopword_ps_stemmed.json','Snowball Stemmer':'without_stopword_sb_stemmed.json',
           'Lancaster Stemmer':'without_stopword_lc_stemmed.json','Customized Stemmer':'without_stopword_custom_stemmed.json'}

        stem_with_stop={'No Stemming': "tokenized.json", 'Porter Stemmer': 'ps_stemmed.json','Snowball Stemmer':'sb_stemmed.json',
           'Lancaster Stemmer':'lc_stemmed.json','Customized Stemmer':'custom_stemmed.json'}
        if flags['stop_words'][0] == True:
            self.data = json.loads(open('stemmers/'+stem_no_stop[flags['stemmer'][0]]).read())
        elif flags['stop_words'][0] == False:
            self.data = json.loads(open('stemmers/'+stem_with_stop[flags['stemmer'][0]]).read())
        self.file_map=json.loads(open('pos_index/'+'file_map.json').read())
        
        self.data1={}
        if zones == None: 
              zones=['TITLE','DESCRIPTION','NOTES','LOCATION']
        
        for d in self.data.keys():
            elist=[]
            for tag in self.data[d].keys():
                if tag in zones:
                    for word_list in self.data[d][tag]:
                        #we should add stopwords if the selected file is note containg stopwords
                        if word_list != 'None':
                            elist.append(word_list)
            self.data1[d]=elist

        self.N = len (self.data1.keys())

        #exctract the list values from all the file to get all the words in our dataset
        #the out will look like this 
        #[[word,word,word],[word,word,word,word],[word....],...]
        fn=[]
        for k in self.data1.keys():
            fn.append(self.data1[k])

        #get the frequncy of all the words
        #the output is like this
        #{'go':5,'rabee':70,'test':20,...}
        self.DF = {}
        for i in range(self.N):
            tokens = fn[i]
            for w in tokens:
                try:
                    self.DF[w].add(i)
                except:
                    self.DF[w] = {i}
        for i in self.DF:
            self.DF[i] = len(self.DF[i])

        self.total_vocab_size = len(self.DF)
        self.total_vocab = [x for x in self.DF]
        
        #create a function to get the frequncy of the word
        #doc_freq('go') will return 1

        
        # tf_idf 
        doc = 0

        tf_idf = {}
        for i in tqdm(range(self.N)):
            
            tokens = fn[i]
            
            counter = Counter(tokens)
            words_count = len(tokens)
            for token in np.unique(tokens):
                
                #tf = counter[token]/words_count
                tf=counter[token]
                df = self.doc_freq(token)
                idf = np.log((self.N+1)/(df+1))
                #idf=np.log(N/df)
                
                tf_idf[doc, token] = tf*idf#weight for large frequncy it will get less weight

            doc += 1

        #create the victor
        self.D = np.zeros((self.N, self.total_vocab_size))
        for i in tqdm(tf_idf):
            try:
                ind = self.total_vocab.index(i[1])
                self.D[i[0]][ind] = tf_idf[i]
            except:
                pass
        Q = self.cosine_similarity(20000,query,flags)
        return Q
        
    def gen_vector(self,tokens):

        Q = np.zeros((len(self.total_vocab)))
        
        counter = Counter(tokens)
        words_count = len(tokens)

        query_weights = {}
        
        for token in tqdm(np.unique(tokens)):
            
            tf = counter[token]/words_count
            df = self.doc_freq(token)
            idf = math.log((self.N+1)/(df+1))

            try:
                ind = self.total_vocab.index(token)
                Q[ind] = tf*idf
            except:
                pass
        return Q
    
    def cosine_sim(self,a, b):
        cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
        return cos_sim

    def cosine_similarity(self,k, query,flags):
        tk=NlpTokenizer()
        
        token = tk.tokenizec(query)
        if flags['stop_words'][0]==1:
            Stopwords=stopwords.words('english')
            token=[item for item in token if item not in Stopwords]
        if flags['stemmer'][0] == 'Porter Stemmer':        
            token=searcher().Porter_Stemmer(token)
        elif flags['stemmer'][0] == 'Snowball Stemmer':        
            token=searcher().Snowball_Stemmer(token)
        elif flags['stemmer'][0] == 'Lancaster Stemmer':
            token=searcher().Lancaster_Stemmer(token)
        elif flags['stemmer'][0] == 'Customized Stemmer':
            token=searcher().Customized_Stemmer(token)   
        
        
        d_cosines = []
        
        query_vector = self.gen_vector(token)
        
        for d in tqdm(self.D):
            #result = 1 - spatial.distance.cosine(query_vector, d)
            result=self.cosine_sim(query_vector, d)
            d_cosines.append(result)
            
        out = np.array(d_cosines).argsort()[-k:][::-1]
        #out = np.array(d_cosines).argsort()
        
                
        #return(out)
        dictt={}
        for index,d in enumerate(self.data1.keys()):
            dictt[index]=d

        fn_list=[]
        fn_cosine=[]
        for i in out:
            fn_list.append(dictt[i])
            fn_cosine.append(d_cosines[i])
        df=pd.DataFrame(list(zip(fn_list,fn_cosine)),columns=['file','cosine'])
        df=df[df['cosine']>0.01]['file']

        org_files=json.loads(open('dataset.json').read())
        docs={}
        for key in df:
            docs[key]=org_files[key]
        
        return docs

    ####################################
# import pandas as pd

# flags=pd.DataFrame(data=np.zeros([1,12]),columns=['boolean','zone_based','cosine','wildcard','stemming','stemmer','proximity','semantic','ontology','exact_match','regex','stop_words'])
# flags['stemmer'][0]='No Stemming'
# cs=cosine_sim()
# x,y=cs.cosine(flags,'dark-skinned boy wearing a black cap and a dark blue and yellow')
