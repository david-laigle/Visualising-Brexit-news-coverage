# -*- coding: utf-8 -*-

from get_guardian_data import GetData # import class from .py file
from tokenize_guardian_data import TokenizeData # import class from .py file
from visualise_guardian_data import VisualiseData # import class from .py file

"""
In order to run this code, you will first need to obtain a Guardian API key
from https://open-platform.theguardian.com/access/ and place it as a string
in the following line of code as the second argument (i.e. API_key='4b32...').
"""

query = GetData(query_terms='Brexit', # place query term(s) here
                API_key=) # place API key here as a string
data = query.get_article_data() # return dataframe

tokens = TokenizeData(input_data=data).tokenize() # return tokens

visuals = VisualiseData(use_data=data, # feed data,
                        use_tokens=tokens, # tokens
                        query_terms=query.query_terms) # and query terms into a new instance

visuals.visualise_trend() # visualise number of articles per month
visuals.visualise_word_frequency() # visualise most frequent words in titles
visuals.visualise_word_cloud() # visualise title words as a word cloud