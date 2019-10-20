# -*- coding: utf-8 -*-

import datetime # import date and time manipulation library
import pandas as pd # import data manipulation and analysis library
import requests # import HTTP request library

class GetData(): # create class

    def __init__(self, query_terms, API_key): # define constructor

        self.page_results = 199 # 199 results per page
        self.query_terms = query_terms.replace(' ', '%20') # URL-friendly query term(s)
        self.API_key = API_key # your API key

    def _create_URL(self, page_number): # define method to create URLs
        
        URL_0 = 'https://content.guardianapis.com/search?page=' # base URL
        URL_1 = str(page_number) # page number
        URL_2 = '&page-size=' # page size
        URL_3 = str(self.page_results) # number of results per page
        URL_4 = '&q=%22' # query
        URL_5 = str(self.query_terms) # query terms
        URL_6 = '%22&api-key=' # API key
        URL_7 = str(self.API_key) # your API key
        URL_c = str(URL_0 + URL_1 + URL_2 + URL_3 + URL_4 + URL_5 + URL_6 + URL_7) # concatenate
        return URL_c # return concatenated URL

    def get_article_data(self): # define method to pull data
        
        d = [] # empty list

        response = requests.get(self._create_URL(page_number=1)) # consult page 1
        page_count = response.json() # read contents
        page_count = page_count['response']['pages'] # get number of pages to be looped over
        
        for i in range(1, page_count+1): # loop over all pages
            try: # attempt to
                response = requests.get(self._create_URL(page_number=i)) # consult page i
                temp = response.json() # read contents
                temp = temp['response']['results'] # select results
                d.append(temp) # append results to list
            except: # if it does not work
                pass # proceed
       
        d = [val for sublist in d for val in sublist] # list comprehension
        df = pd.DataFrame(d) # store as dataframe
        df.sort_values(['webPublicationDate'], ascending=False, inplace=True) # sort dataframe then reformat datetime values
        df['Date'] = df.apply(lambda row: datetime.datetime.strptime(row.webPublicationDate[0:10], '%Y-%m-%d').date(), axis=1)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce') # store 'Date' column as datetime
        df = df[['Date', 'webTitle']] # retain two columns
        df.columns = ['Date', 'Title'] # name columns
        df.drop_duplicates(inplace=True) # drop duplicates
        df.reset_index(inplace=True, drop=True) # reset dataframe index
        return df # return dataframe