# -*- coding: utf-8 -*-

import datetime # import date and time manipulation library
import matplotlib.pyplot as plt # import plotting library
import nltk # import Natural Language Processing library
import numpy as np # import scientific computing library
import pandas as pd # import data manipulation and analysis library
from wordcloud import WordCloud, STOPWORDS # import word cloud library

class VisualiseData(): # create class
    
    def __init__(self, use_data, use_tokens, query_terms): # define constructor

        self.df = use_data # dataframe
        self.tokens = use_tokens # tokens
        self.query_terms = query_terms # query term(s)
        
    def visualise_trend(self): # define method to visualise number of articles per month
        
        df = self.df # shorten dataframe name
        
        plt.figure(figsize=(10,3), dpi=100) # set figure size and resolution
        
        year_month = pd.date_range(df.Date.min()-datetime.timedelta(days=31), df.Date.max(), freq='MS').tolist() # create date range
        year_month = [datetime.date.fromtimestamp(datetime.datetime.timestamp(i)) for i in year_month] # list comprehension
        year_month = pd.DataFrame(year_month) # convert to dataframe
        year_month.columns = ['Date'] # name column
        
        article_count = df.groupby(by=[df.Date.dt.year, df.Date.dt.month]).count() # group by count
        article_count = article_count.unstack(fill_value=0).stack() # fill missing slots with zeros
        dates = [datetime.date(i[0],i[1],1) for i in article_count.index] # create date for each year month combination
        values = [i for i in article_count.Title] # list comprehension
        article_count = pd.DataFrame({'Date': dates, 'Articles':values}) # convert to dataframe
        
        month_data = year_month.merge(article_count, on='Date', how='left') # merge dataframes
        month_data.fillna(0.0) # fill NaN with zeros
        
        plt.plot( # plot line
                 [i for i in month_data.Date], # with monthly intervals as x
                 [i for i in month_data.Articles], # and number of articles as y
                 color='grey' # in colour
                 )

        plt.axhline( # plot line representing average number of articles per month
                    y=df.groupby(by=[df.Date.dt.month, df.Date.dt.year]).count().mean()[0], 
                    color='orangered', # in colour,
                    linestyle='-', # style,
                    linewidth=2, # linewidth,
                    label="Average number of articles per month" # label
                    )
        
        plt.annotate( # annotate
                    'Month in progress', # string
                     xy=( # pointing at x = current month and y = number of articles so far this month
                         datetime.datetime.now()-datetime.timedelta(days=int(datetime.datetime.now().day)-1),
                         np.trim_zeros(list(df.groupby(by=[df.Date.dt.year, df.Date.dt.month]).count()['Title'].unstack(fill_value=0).stack()))[-1]
                         ),
                     xytext=(-100, -50), # with string displayed at x, y
                     textcoords='offset points', # with xytext coordinates relative to xy coordinates
                     bbox=dict(boxstyle='round', edgecolor='black', fc='white'), # with text box
                     arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0') # and arrow
                     )
        
        plt.legend(loc=2, edgecolor='black') # include legend
        plt.xlabel("\nYear") # set x label
        plt.ylabel("Number of articles\n") # set y label
        plt.title('Guardian articles about '+str(self.query_terms).replace('%20', ' ').title()+'\n', # set title
                  fontsize=15) # in font size
        output_name = str(self.query_terms).lower().replace(' ', '_').replace('%20', '_')+'_trend_' # create output name
        output_name = output_name+str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+'.png' # create output name
        plt.savefig(output_name, dpi=300, bbox_inches='tight') # save output as .png file in Current Working Directory
        plt.show() # show plot

    def visualise_word_frequency(self): # define method to visualise most frequent words in article titles
        
        freq = nltk.FreqDist(self.tokens) # create frequency dictionary
        freq.pop(str(self.query_terms).lower(), None) # optional, remove single query term from dictionary
        top_freq = {key: freq[key] for key in sorted(freq, key=freq.get, reverse=True)[:25]} # retain top 25 key-value pairs
        top_freq = pd.DataFrame({'keyword': [i for i in top_freq.keys()], # build dataframe from keys
                                'frequency':[i for i in top_freq.values()]}) # values
        top_freq.sort_values(['frequency'], ascending=True, inplace=True) # sort by value
        
        plt.figure(figsize=(8, 6)) # set figure size
        plt.barh(top_freq.keyword, top_freq.frequency) # create bar chart
        plt.xlabel("\nFrequency") # set x label
        plt.ylabel("Keyword\n") # set y label
        plt.title(str(self.query_terms).replace('%20', ' ').title()+' word frequency\n', fontsize=15) # set title
        output_name = str(self.query_terms).lower().replace(' ', '_').replace('%20', '_')+'_word_frequency_' # create output name
        output_name = output_name+str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+'.png' # create output name
        plt.savefig(output_name, dpi=300, bbox_inches='tight') # save output as .png file in Current Working Directory
        plt.show() # show plot
        
    def visualise_word_cloud(self): # define method to visualise title words as a word cloud

        wordcloud = WordCloud( # create word cloud
                              width=4000, # width
                              height=4000, # height,
                              background_color='white', # background colour
                              stopwords=STOPWORDS, # remove stopwords
                              min_font_size=10 # set minimum font size
                              ).generate(' '.join(self.tokens)) # from string formed by concatenated tokens
                            
        plt.figure(figsize=(8,8), dpi=300) # set figure size and resolution
        plt.imshow(wordcloud) # display image
        plt.axis("off") # hide axis
        plt.title(str(self.query_terms).replace('%20', ' ').title()+' word cloud\n', fontsize=15) # set title
        output_name = str(self.query_terms).lower().replace(' ', '_').replace('%20', '_')+'_word_cloud_' # create output name
        output_name = output_name+str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+'.png' # create output name
        plt.savefig(output_name, dpi=300, bbox_inches='tight') # save output as .png file in Current Working Directory
        plt.show() # show plot