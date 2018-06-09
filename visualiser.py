# -*- coding: utf-8 -*-
"""
Created on         : 19/05/2018
Last modified on   : 27/05/2018
Author             : Satyabrat Borgohain
Description :
    
    This class visulises the results of the previous analysis done by the other
    classes. It is used to help extract the stylometrics of the different works.

    Objects of this class can be created for standalone puposes.
"""



import string
import pandas as pd
from lxml import html
import requests

class AnalysisVisualiser:
    """A visualiser class with methods to visualise and produce plots for analysis
    at different levels across a number of tokenised works.
    
    """
    
    def __init__(self, all_text_stats):
        """Creates a AnalysisVisualiser object, a dataframe of dataframe, containing
        all analysis statistics, which needes to be passed during the initialisation.
        
        Arguments:
            all_text_stats (pandas DataFrame): The list of tokens.
        
        """

        self.all_stats = all_text_stats.copy()
        #Storing the works (different written texts)
        self.works = self.all_stats['work'].tolist()
    
    
    def visualise_character_frequency(self):
        """Visualises the character frequencies across all the works.
    
        Function for visualising the occurrence of characters (alphabets and 
        numerals) for all the texts provided. The relative frequency is considered
        i.e. occurence of a character / total characters in the text.
        
        It creates two bar charts and a line graph for ease of analysis and
        inference.
    
        Punctuations are not considered during in this method. 
    
        """
        
        #Location of the character frequency column in the df
        j = self.all_stats.columns.get_loc("char_freq")
        
        for i in range(0,len(self.all_stats)):
            temp_df = self.all_stats.iloc[i, j]
            #Droping all rows with punctuations based on ASCII order of characters
            temp_df.drop(temp_df[(temp_df.character < '0') | (temp_df.character > 
                                 '9') & (temp_df.character < 'A') | 
                                (temp_df.character > 'Z')].index, inplace=True)

        
            #Convert occurences to frequencies
            total = self.all_stats.iloc[i, j]['occurence'].sum()
            self.all_stats.iloc[i, j]['occurence'] = self.all_stats.iloc[i, j]['occurence'].map(lambda x: x / total)
        
        df_columns = dict([(x,list(self.all_stats.iloc[idx, j]['occurence'])) for idx,x in enumerate(self.works)])
        df = pd.DataFrame(df_columns, index=list(string.ascii_uppercase+string.digits))
        
        # Filtering all rows with only zeros and discarding them
        df = df[(df.T != 0).any()]
        
        #Plotting graphs
        #1. Bar chart - with subplots
        df.plot.bar(rot=0,subplots=True,sharey=True,width=0.9,title=['Relative Character frequencies']+
                    ['']*(len(self.all_stats)-1),figsize=(12, 10))
        #2. Bar chart - without subplots
        df.plot.bar(rot=0,figsize=(20, 10),title='Relative Character frequencies')
        #3. Line chart
        df.plot.line(rot=0,figsize=(12, 10),title='Relative Character frequencies')
        
        
    def visualise_punctuation_frequency(self):
        """Visualises the punctuation frequencies across all the works.
    
        Function for visualising the occurrence of punctuations for all the texts 
        provided. The relative frequency is considered i.e. occurence of a 
        punctuation / total characters in the text.
        
        It creates two bar charts and a line graph for ease of analysis and
        inference.
    
        """
        
        j = self.all_stats.columns.get_loc("punc_freq")
        k = self.all_stats.columns.get_loc("char_freq")
        
        #Converting occurences to frequencies
        for i in range(0,len(self.all_stats)):
            total = self.all_stats.iloc[i, k]['occurence'].sum()
            self.all_stats.iloc[i, j]['occurence'] = self.all_stats.iloc[i, j]['occurence'].map(lambda x: x / total)
        
        df_columns = dict([(x,list(self.all_stats.iloc[idx, j]['occurence'])) for idx,x in enumerate(self.works)])
        df = pd.DataFrame(df_columns, index=list(string.punctuation))
        
        # Filtering all rows with only zeros and discarding them
        df = df[(df.T != 0).any()]
        
        #Plotting graphs
        #1. Bar chart - with subplots
        df.plot.bar(rot=0,subplots=True,sharey=True,width=0.9,title=['Relative Punctuation frequencies']+['']*(len(self.all_stats)-1),figsize=(12, 10))
        #2. Bar chart - without subplots
        df.plot.bar(rot=0,figsize=(20, 10),title='Relative Punctuation frequencies')
        #3. Line chart
        df.plot.line(rot=0,figsize=(12, 10),title='Relative Punctuation frequencies')
        
        
    def visualise_stopword_frequency(self):
        """Visualises the stopword frequencies across all the works.
    
        Function for visualising the occurrence of stopwords for all the texts 
        provided. The relative frequency is considered i.e. occurence of a 
        stopword / total words in the text.
        
        It creates two bar charts for ease of analysis and inference.
    
        """
        
        #Stopwords taken from : http://www.lextek.com/manuals/onix/stopwords1.html
        html_page = requests.get('http://www.lextek.com/manuals/onix/stopwords1.html')
        dom = html.fromstring(html_page.content)
        stopwords = dom.xpath('//pre/text()')[0]
        stopwords = stopwords.split('\n')
        #Extracting only the stopwords and storing in a list
        stopwords = [x.upper() for x in stopwords if x != '' and not x.startswith('#')]
        
        j = self.all_stats.columns.get_loc("stop_freq")
        k = self.all_stats.columns.get_loc("word_len_freq")
        
        #Convert occurrences to frequencies
        for i in range(0,len(self.all_stats)):
            total = self.all_stats.iloc[i, k]['occurence'].sum()
            self.all_stats.iloc[i, j]['occurence'] = self.all_stats.iloc[i, j]['occurence'].map(lambda x: x / total)
        
        df_columns = dict([(x,list(self.all_stats.iloc[idx, j]['occurence'])) for idx,x in enumerate(self.works)])
        df = pd.DataFrame(df_columns, index=stopwords)
        
        # Filtering all rows with only zeros and discarding them
        df = df[(df.T != 0).any()]
        
        #1. Bar chart - with subplots
        df.plot.bar(rot=90,subplots=True,sharey=True,width=0.9,title=['Relative Stopword frequencies']+['']*(len(self.all_stats)-1),figsize=(20, 10))
        #2. Bar chart - without subplots
        df.plot.bar(rot=90,figsize=(20, 10),title='Relative Stopword frequencies')
        
    
    def visualise_word_length_frequency(self):
        """Visualises the word length frequencies across all the works.
    
        Function for visualising the occurrence of words of similar lengths for 
        all the texts provided. The relative frequency is considered i.e. occurence
        of a wordlength / total words in the text.
        
        It creates two bar charts for ease of analysis and inference.
    
        """
        
        j = self.all_stats.columns.get_loc("word_len_freq")
        
        #Convert occurences to frequencies
        for i in range(0,len(self.all_stats)):
            total = self.all_stats.iloc[i, j]['occurence'].sum()
            self.all_stats.iloc[i, j]['occurence'] = self.all_stats.iloc[i, j]['occurence'].map(lambda x: x / total)
        
        df_columns = dict([(x,list(self.all_stats.iloc[idx, j]['occurence'])) for idx,x in enumerate(self.works)])
        df = pd.DataFrame(df_columns, index=range(0,40))
        
        # Filtering all rows with only zeros and discarding them
        df = df[(df.T != 0).any()]
        
        #1. Bar chart - with subplots
        df.plot.bar(rot=0,subplots=True,sharey=True,width=0.9,title=['Relative Word length frequencies']+['']*(len(self.all_stats)-1),figsize=(12, 10))
        #2. Bar chart - without subplots
        df.plot.bar(rot=0,figsize=(20, 10),title='Relative Word length frequencies')
        #3. Line chart
        df.plot.line(rot=0,figsize=(12, 10),title='Relative Word length frequencies')
        