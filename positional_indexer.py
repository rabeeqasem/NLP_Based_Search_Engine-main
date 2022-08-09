import nltk
from nltk.corpus import stopwords
import re
import os
import numpy as np
import json
from tokenizec import NlpTokenizer

Stopwords = set(stopwords.words('english'))

class pos_index ():

    def pos_indexer(self,data, flag):   
        # In this example, we create the positional index for only 1 folder. 
        
        # Initialize the file no. 
        fileno = 0
        
        # Initialize the dictionary. 
        pos_index = {} 
        
        # Initialize the file mapping (fileno -> file name). 
        file_map = {} 
        
        # 	# For every file. 
        # for doc in data:
        #     sentence = ''
        #     for keys in data[doc]:
        #         if keys in ['TITLE','DESCRIPTION','NOTES']:
        #             short_text = data[doc][keys]
        #             if short_text is not None:
        #                 sentence = sentence + data[doc][keys]+' '
        
           
        #     final_token_list = NlpTokenizer.tokenizec(sentence)
        for key in data.keys():
            for tag in data[key]:
                if tag in ['TITLE','DESCRIPTION','NOTES','LOCATION']:
                    final_token_list = [word.lower() for word in data[key][tag]] ## lower 
                    ## optinal for user
                    if flag == 1: 
                        final_token_list = [word for word in final_token_list if word not in Stopwords]
                    # For position and term in the tokens. 
                    for pos, term in enumerate(final_token_list):         
                        # If term already exists in the positional index dictionary. 
                        if term in pos_index: 
                            # Increment total freq by 1. 
                            pos_index[term][0] = pos_index[term][0] + 1
                            # Check if the term has existed in that DocID before. 
                            if fileno in pos_index[term][1]:
                                if tag in pos_index[term][1][fileno]:
                                    pos_index[term][1][fileno][tag].append(pos) 
                                else:
                                    pos_index[term][1][fileno].update({tag:[pos]})
                            else:
                                pos_index[term][1].update({fileno:{tag:[pos]}})
        
                        # If term does not exist in the positional index dictionary 
                        # (first encounter). 
                        else:         
                            # Initialize the list. 
                            pos_index[term] = [] 
                            # The total frequency is 1. 
                            pos_index[term].append(1) 
                            # The postings list is initially empty. 
                            pos_index[term].append({})	 
                            # Add doc ID to postings list.
                            pos_index[term][1][fileno]={tag:[pos]}
                            
            # Map the file no. to the file name. 
            file_map[fileno] = list(data.keys())[fileno]
            # Increment the file no. counter for document ID mapping
            fileno += 1

        return file_map, pos_index

