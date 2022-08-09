import nltk
from nltk.corpus import stopwords
import json
from sklearn.feature_extraction.text import CountVectorizer
from tokenizec import NlpTokenizer




def createfolder(text):
    from nltk.corpus import stopwords

    path='{}.json'.format(text)
    f = open(path,)
    data = json.load(f)

    stopwords=stopwords.words('english')
    Data_withoutstopwords={}

    for fn in data.keys():
        
        tags_values={}
        for tag in data[fn].keys():
            list=[]
            for values in data[fn][tag]:
                if values not in stopwords:
                    list.append(values)
            tags_values[tag]=list
        Data_withoutstopwords[fn]=tags_values


    out_path='without_stopword_{}.json'.format(text)

    with open(out_path,'w')as json_file:
        json.dump(Data_withoutstopwords, json_file,indent=4)
    

                
filenames=['ps_stemmed','custom_stemmed','lc_stemmed','sb_stemmed','tokenized']
for fn in filenames:
    createfolder(fn)        

                
                    

