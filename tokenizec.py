import re
import json
class NlpTokenizer:
    #toknize single string for example (rabee loai hindi )
    #the function recive  a string text
    def tokenizec(self,text):
        regx="\w\w*[.|:|?|'||...|!|-|()]?\w\w*"
        tk=re.findall(regx,text)
        tk=[item.lower() for item in tk]
        return tk

    #this function return set list of tokens (remove dublicates tokenz)
    #the function recive  a string text
    def unitoknizer(self,text):
        ListOfTokens=self.tokenizec(text)
        SetTkn=set(ListOfTokens)
        return SetTkn
    
    #this functino return list of token for a single file for example data['3843.eng']
    def singlefiletk(self,single_file): 
        listt=[]
        for tag in single_file.keys():
            listt.append(single_file[tag])
        string=' '.join(map(str, listt))
        listt=self.unitoknizer(string)
        #listt=self.tokenizec(string)
        return listt

    #used to tokenize the whole document, input is a dictionary
    def datatoken(self,datafile):
        list1={}
        for fn  in datafile.keys():
            tags=[]
            tokens=[]
            for tag in datafile[fn]:
                tokens.append(self.tokenizec(str(datafile[fn][tag])))
                tags.append(tag)
            list1[fn]=dict(zip(tags,tokens))
                
        return list1





'''

nt=NlpTokenizer()
f = open('E:/Master/NLP/project/iaprtc12/iaprtc12/xyz.json',) 
data = json.load(f)
listt=nt.singlefiletk(data['3843.eng'])
print(listt)
#listt=nt.datatoken(data)
#print(len(listt))
'''