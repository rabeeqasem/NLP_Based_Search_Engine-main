import requests 
import nltk 
from bs4 import BeautifulSoup 
import sys
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import SnowballStemmer
from tokenizec import NlpTokenizer
from custom_stemmer import customized_stemmer

from nltk.corpus import wordnet

stem_words = []

class searcher():    
   
    #check the text if URL or normail text 
    def check_text(self,text):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
        flag = re.match(regex,text.strip()) is not None  # True
        return flag
    
    
    def if_url(self,text):
        page = requests.get(text)
        soup = BeautifulSoup(page.content,'html.parser')
        return soup.get_text()
    
    
    def if_text(self,text):
        tokens = self.token_fun(text)
        return tokens
    
    def token_fun(self,words):
        
        tokens = nltk.word_tokenize(words)
        return tokens
      
    def Porter_Stemmer(self,data):
        porter = PorterStemmer()
        tk=NlpTokenizer()
        if type(data) == dict:                        
            data_tokens=tk.datatoken(data)
            stem_data={}
            for file in data_tokens.keys():
                stems=[]
                tags=[]
                for tag in data_tokens[file]:
                    stemmed=[]
                    for token in data_tokens[file][tag]:
                        stemmed.append(porter.stem(token))
                    stems.append(stemmed)
                    tags.append(tag)
                    
                stem_data[file]=dict(zip(tags,stems))
            return stem_data
        else:
            stem_words=[]
            for w in data: 
                stems = porter.stem(w) 
                stem_words.append(stems) 
            return stem_words
    
    
    def Snowball_Stemmer(self,data):
        snowball= SnowballStemmer(language='english')
        tk=NlpTokenizer()
        if type(data) == dict:                        
            data_tokens=tk.datatoken(data)
            stem_data={}
            for file in data_tokens.keys():
                stems=[]
                tags=[]
                for tag in data_tokens[file]:
                    stemmed=[]
                    for token in data_tokens[file][tag]:
                        stemmed.append(snowball.stem(token))
                    stems.append(stemmed)
                    tags.append(tag)
                    
                stem_data[file]=dict(zip(tags,stems))
            return stem_data
        else:
            stem_words=[]
            for w in data: 
                stems = snowball.stem(w) 
                stem_words.append(stems) 
            return stem_words
    
    def Lancaster_Stemmer(self,data):
        lancaster=LancasterStemmer()
        tk=NlpTokenizer()
        if type(data) == dict:                        
            data_tokens=tk.datatoken(data)
            stem_data={}
            for file in data_tokens.keys():
                stems=[]
                tags=[]
                for tag in data_tokens[file]:
                    stemmed=[]
                    for token in data_tokens[file][tag]:
                        stemmed.append(lancaster.stem(token))
                    stems.append(stemmed)
                    tags.append(tag)
                    
                stem_data[file]=dict(zip(tags,stems))
            return stem_data
        else:
            stem_words=[]
            for w in data: 
                stems = lancaster.stem(w) 
                stem_words.append(stems) 
            return stem_words
     
    def Customized_Stemmer(self, data):
        my_stem = customized_stemmer()
        stem_data = my_stem.my_stemmer(data)
        return stem_data

    
  
