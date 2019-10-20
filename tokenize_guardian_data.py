# -*- coding: utf-8 -*-

import re # import regular expression manipulation library
from nltk.corpus import stopwords # import list of stopwords
from nltk.tokenize import word_tokenize # import tokenizer

class TokenizeData(): # create class
    
    def __init__(self, input_data): # define constructor
        
        self.df = input_data # dataframe
        
    def tokenize(self): # define method to tokenize data

        tokens = [] # empty list
        
        for i in range(len(self.df.Title)): # for all article titles
            temp = self.df.Title[i] # temp = title
            if '|' in temp: temp = temp[:temp.find('|')] # remove words after '|'
            temp = re.sub('[^A-Za-z]',' ', temp) # remove non-alphabetical characters
            temp = word_tokenize(temp.lower()) # tokenize and lowercase words
            tokens.append(temp) # append token to list
        
        tokens = [val for sublist in tokens for val in sublist] # list comprehension
        tokens = [word for word in tokens if word not in stopwords.words('english')] # remove stopwords
        
        additional_stopwords = [ # define additional stopwords
                                'guardian', 'view', 'briefing', 'brief',
                                'editorial', 'live', 'updates', 'observer',                                
                                'review', 'happened', 'morning', 'mail',
                                'weekly', 'could', 'would', 'must', 'say', 
                                'says', 'get', 'make', 'take', 'know',
                                'come', 'show', 'like', 'still'
                                ]
        
        tokens = [word for word in tokens if word not in additional_stopwords] # remove stopwords
        
        return tokens # return tokens