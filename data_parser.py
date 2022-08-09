
import pandas as pd
import xml.etree.ElementTree as et
import os
import tqdm
import json
from check_search import searcher
from tokenizec import NlpTokenizer
from positional_indexer import pos_index
from tqdm import tqdm

main_path='annotations_complete_eng/'
entries = os.listdir(main_path)
path=[]
Cols=['DOCNO','TITLE','DESCRIPTION','NOTES','LOCATION','DATE','IMAGE','THUMBNAIL']
dataset=pd.DataFrame(data=None, columns=Cols)
indexed={}
subdic={}
for folder in entries:
    sub=os.listdir(main_path+folder+'/')
    for file in sub:
        filename = main_path+folder+'/'+file 
        with open(filename, 'r') as content:
            root = et.parse(content).getroot()
            path.append(filename)
            subdic={}
            for col in Cols:
                value = root.find(col).text
                #if value is not None: value=value.lower()
                subdic[col]=value
            indexed[file]=subdic



with open('dataset.json', 'w') as json_file:
  json.dump(indexed, json_file,indent=4)

#data = json.loads(open("tokenized.json").read())


#--------------------------------------------------------------#
#this code for stemming dataset and save it offline

tk=NlpTokenizer()
tokens= tk.datatoken(indexed)
with open('tokenized.json', 'w') as json_file:
  json.dump(tokens, json_file,indent=4)

sr=searcher()
ps_stemmed=sr.Porter_Stemmer(indexed)
with open('ps_stemmed.json', 'w') as json_file:
  json.dump(ps_stemmed, json_file,indent=4)

sb_stemmed=sr.Snowball_Stemmer(indexed)
with open('sb_stemmed.json', 'w') as json_file:
  json.dump(sb_stemmed, json_file,indent=4)

lc_stemmed=sr.Lancaster_Stemmer(indexed)
with open('lc_stemmed.json', 'w') as json_file:
  json.dump(lc_stemmed, json_file,indent=4)

custom_stemmed=sr.Customized_Stemmer(indexed)
with open('custom_stemmed.json', 'w') as json_file:
  json.dump(custom_stemmed, json_file,indent=4)


#----------------------------------------------------#
#positional indexers


stem_no_stop=['without_stopword_tokenized.json', 'without_stopword_ps_stemmed.json', 'without_stopword_sb_stemmed.json',
           'without_stopword_lc_stemmed.json', 'without_stopword_custom_stemmed.json']

stem_with_stop=['tokenized.json', 'ps_stemmed.json', 'sb_stemmed.json', 'lc_stemmed.json', 'custom_stemmed.json']


pos=pos_index()

for file in tqdm(stem_no_stop):
    data=json.loads(open("stemmers/"+file).read())
    file_map, index=pos.pos_indexer(data, 0)
    with open('pos_index/pos_'+file, 'w') as json_file:
      json.dump(index, json_file,indent=4)

for file in tqdm(stem_with_stop):
    data=json.loads(open("stemmers/"+file).read())
    file_map, index=pos.pos_indexer(data, 0)
    with open('pos_index/pos_'+file, 'w') as json_file:
      json.dump(index, json_file,indent=4)
      
with open('pos_index/file_map.json', 'w') as json_file:
  json.dump(file_map, json_file,indent=4)



'''
file = "E:/Master/NLP/project/iaprtc12/iaprtc12/"
file_name="dataset"+'.csv'
if not os.path.exists(file):
    os.makedirs(file)
dataset.to_csv(file+file_name)
'''