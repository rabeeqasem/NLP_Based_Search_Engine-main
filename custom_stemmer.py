
from nltk.corpus import stopwords
import re
from tokenizec import NlpTokenizer
from tqdm import tqdm


stop_words= stopwords.words('english')
# import dectionary
dictionary= open('words.txt').readlines()

for i in range(0,len(dictionary)):
    dictionary[i]= dictionary[i].strip().lower() 
dictionary=[x for x in dictionary if len(x)>1]

# import stop words
stop_words=open('stopwords.txt').readlines()
for i in range(len(stop_words)):
    stop_words[i]= stop_words[i].strip().lower() 


class customized_stemmer():
    
    def sfx_stem(self,text,sfx):
        #print( text , sfx)
        reg_ex='('+sfx+')$' #create regular expression to be subtracted from the text
        l=len(sfx)
        if (text[-l-1]==text[-l-2] )and( text[-l-1] not in ['a','e','o','u','i','x','y','w'] )and (text[-l-3] in ['a','e','o','u','i']):
             #check doubled consonant like flipped
             return text[:-l-1]
        elif re.sub(reg_ex,'e',text) in dictionary  and text[-l-1] not in ['a','e','o','u','i','x','y','w']  :
            #to check if there is removed vowel like "taking" 
            return re.sub(reg_ex,'e',text)
        elif (text[-l-1]=='i' )and( text[-l-2] not in ['a','e','o','u','i'] and sfx not in['tion','tional']):
             #to check if there is consonant followed by y letter like studied
            return re.sub('('+'i'+sfx+')$','y',text)
        elif text[-l-1]=='y' and len(re.sub('('+sfx+')$','',text))<3 and re.sub('('+'y'+sfx+')$','ie',text) in dictionary :
             #to check if the y is from ie like die --> dying
             return re.sub('('+'y'+sfx+')$','ie',text)
        elif sfx=='s' and text[-l-2:-l] =='ie' and text[-l-3] not in ['a','e','o','u','i']:
             # for words ends with consonant and y that is changed to ie like accompany --> accompanies
             return re.sub('(ies)$','y',text)    
         #rules for tion, tional   
        elif sfx in ['tion','tional'] and text[-l-1:-l]=='a' and text[-l-2:-l]=='iz':
             # ize followed by tion or tional like authorize --> authorization
             return  re.sub('('+'a'+sfx+')$','e',text) 
        elif (sfx in ['tion','tional'] and text[-l-1:-l]=='a' ) :
             if text[-l-3:-l-1]=='ic':
                  # ify followed by tion or tional like amplify --> amplification
                 return  re.sub('('+'ica'+sfx+')$','y',text) 
             elif text[-l-3:-l-1]=='am': 
                  # ify followed by tion or tional like acclaim --> acclamation
                 return  re.sub('('+'ama'+sfx+')$','aim',text)
             else: return re.sub('('+sfx+')$','te',text)
        elif (sfx in ['tion','tional'] and text[-l-2:-l]=='ac'):
             # ify followed by tion or tional like liquefy --> liquefaction
             return  re.sub('('+'ac'+sfx+')$','y',text)        
        elif sfx in ['tion','tional'] and text[-l-3:-l] in ['cep','ump','duc','olu','osi']:
             # verbs like        
             if text[-l-3:-l]==['cep']: return re.sub('('+'p'+sfx+')$','ive',text)   #conceive --> conception
             elif text[-l-3:-l]=='ump': return re.sub('('+'p'+sfx+')$','e',text)   #assume --> assumption
             elif text[-l-3:-l]=='duc': return re.sub('('+sfx+')$','e',text)   #deduce --> deduction
             elif text[-l-3:-l]=='olu': return re.sub('('+'u'+sfx+')$','ve',text)   #absolve→absolution
             elif text[-l-3:-l]=='osi': return re.sub('('+'i'+sfx+')$','e',text)   #compose→composition
             else: return re.sub('('+'i'+sfx+')$','e',text)   # compose→composition                
        elif sfx in ['tion','tional'] and text[-l-1:-l+1]in['at','et','ut','it','ot']:
             # verbs end with ate like abbreviate -->abbreviation   complete→completion attribute→attribution
             return re.sub(reg_ex,'t',text) 
        elif sfx in ['tion','tional'] and text[-l-5:-l]=='scrip':
             # verbs end with ate like subscribe --> subscription
             return re.sub('('+'p'+sfx+')$','be',text)     
        elif sfx in ['tion','tional'] and text[-l-1:-l+1] in ['pt','ct'] :
             # verbs end with ate like adopt --> adoption   abstract --> abstraction
             return re.sub(reg_ex,'t',text) 
  
        #ity rules 
        #check bits , sequenty, access 
         
        else: 
             # remove the suffex without changing the text
             return re.sub(reg_ex,'',text) 
     
    
    def checker(self,sfx,token,sensitivity):
            stemmed_token=""           
            if len(sfx) and len(token)>=3:
                #if a suffix is found
                if (len(sfx)/len(token))>sensitivity: #above threshold
                    if re.sub('('+sfx+')$','',token) in dictionary: 
                        stemmed_token=re.sub('('+sfx+')$','',token)
                    elif token.lower() not in stop_words and (len(token)-len(sfx))>=3 and self.sfx_stem(token,sfx) in dictionary:
                        stemmed_token=self.sfx_stem(token,sfx)
                    elif len(token)> len(sfx)+3:
                        stemmed_token=self.sfx_stem(token,sfx) 
                else:
                    stemmed_token=self.sfx_stem(token,sfx) 
            return stemmed_token
        
    def stemmer (self,token_set,sensitivity):    
        
        if type(token_set)== list:
            for i in range(len(token_set)):
                #find suffixes using reg_ex
                sfx=''
                sfx=''.join(re.findall('(s|ed|es|ing|ment|tional|al|er|ly|ness|ity|ship|able|tion|es)$',token_set[i],flags=re.IGNORECASE))
                if len(sfx):
                    token_set[i]=self.checker(sfx, token_set[i], sensitivity)
                
        else:
            sfx=''
            sfx=''.join(re.findall('(s|ed|es|ing|ment|tional|al|er|ly|ness|ity|ship|able|tion|es)$',token_set,flags=re.IGNORECASE))
            if len(sfx):
                token_set=self.checker(sfx, token_set, sensitivity)
                        
        return  token_set
    
    def my_stemmer (self, data):
        tk=NlpTokenizer()
        if type(data) == dict:                        
            data_tokens=tk.datatoken(data)
            stem_data={}
            
            for file in tqdm(data.keys()):
                stems=[]
                tags=[]
                for tag in data_tokens[file]:
                    stemmed=[]
                    for token in data_tokens[file][tag]:
                        stemmed.append(self.stemmer(token,0.4))
                    stems.append(stemmed)
                    tags.append(tag)
                    
                stem_data[file]=dict(zip(tags,stems))
            return stem_data
        else:   
            stem_words= self.stemmer(data,0.4) 
            return stem_words
        
