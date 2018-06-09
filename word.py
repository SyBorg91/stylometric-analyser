# -*- coding: utf-8 -*-
"""
Created on         : 19/5/2018
Last modified on   : 27/5/2018
Author             : Satyabrat Borgohain
Description :
  
    This class creates objects for visualising all the statistics analysed by the
    other classes for characters, punctuation, wordlength and stopwords frequency.

    Objects of this class can be created for standalone puposes.
"""



import pandas as pd
from collections import Counter
import requests
from lxml import html
import re

class WordAnalyser:
    """A analyser class for analysing tokenised input at the 'word' level.
    
    """
    
    def __init__(self):
        """Initializes a WordAnalyser object which is a pandas DataFrame 
        with two columns as : 'word' which contains the word and 
        'occurrence' which holds its corresponding occurrence in the tokenised list.
        
        """
        
        self.word_occ = pd.DataFrame(columns=['word','occurence'])
        
        
    def __str__(self):
        """Prints the word occurrences as a formatted string.
    
        Returns:
            The word occurence dataframe as a formatted string.
    
        """
        
        prefix = 'Word occurences : \n' + "======================\n"
        suffix = "\n======================"
        return prefix + self.word_occ.to_string(index=False, justify='left') + suffix
        
    
    def analyse_words(self, tokenised_list):
        """Analyses the tokenised list for word occurrence.
    
        Function for analysing the given tokenised list and record the number of
        times a word has appeared in the tokens. It records the occurrences
        in the instance variable.

        Arguments:
            tokenised_list (list): The list of tokens.
    
        """
        
        #Finding the word count in the tokenised list
        #Regex allows only alphabets, numerals, ' and -
        word_count=Counter([token.upper() for token in tokenised_list if 
                            re.match("^\d*['-]*[a-zA-Z][a-zA-Z0-9'-]*$", token)])
        
        
    
        #Updating the instance variable with the word occurrences
        self.word_occ = pd.DataFrame(list(word_count.items()), columns=['word', 'occurence'])
                

    def get_stopword_frequency(self):
        """Getter and analysis of the stopword frequency in the tokenised list.
    
        Function for analysing the stopwords occurrence in the tokenised list.
    
        Returns:
            stop_occ (pandas DataFrame): The dataframe of stopword occurrence.
    
        """
        
        #Stopwords taken from : http://www.lextek.com/manuals/onix/stopwords1.html
        html_page = requests.get('http://www.lextek.com/manuals/onix/stopwords1.html')
        dom = html.fromstring(html_page.content)
        stopwords = dom.xpath('//pre/text()')[0]
        stopwords = stopwords.split('\n')
        #Extracting only the stopwords and storing in a list
        stopwords = [x.upper() for x in stopwords if x != '' and not x.startswith('#')]

        #Initializing dataframe to store the stopword occurences only
        stop_occ = pd.DataFrame({'stopword': stopwords,
                                 'occurence': [0]*len(stopwords)})
        #Getting the indices of all stop words in the instance variable
        indices = pd.Index(stop_occ['stopword'].tolist())
        for i, row in self.word_occ.iterrows():
            if row['word'] in stopwords:
                #Get the index of the stopword in the new dataframe
                index = indices.get_loc(row['word'])
                # Assign the occurence of that word
                stop_occ.iloc[index,stop_occ.columns.get_loc("occurence")] = row['occurence']
        
        return stop_occ
        
    
    def get_word_length_frequency(self):
        """Getter and analysis of the word length frequency in the tokenised list.
    
        Function for analysing the tokenised list for the frequency of the times
        words of specific lengths are occurring.
    
        Returns:
            wl_occ (pandas DataFrame): The dataframe of wordlength occurrence.
    
        """
        
        #Initializing a df with max word length of 20
        wl_occ = pd.DataFrame({'wordlength': range(0,40),
                                 'occurence': [0]*40})
        
        word_len_occ = self.word_occ.copy()
        #Function to calculate the length of each words
        get_length = lambda x: len(x)
        #Function to convert/coerce occurence datatype to integer
        to_integer = lambda y: int(y)
        word_len_occ['word'] = word_len_occ['word'].map(get_length)
        word_len_occ['occurence'] = word_len_occ['occurence'].map(to_integer)
        #Renaming the 'word' column
        word_len_occ = word_len_occ.rename(columns={'word': 'wordlength'})
        #Grouping the words with similar lengths and getting the sum of occurence
        word_len_occ = word_len_occ.groupby('wordlength').sum().reset_index()
        
        indices = pd.Index(wl_occ['wordlength'].tolist())
        for i, row in word_len_occ.iterrows():
            if row['occurence'] != 0:
                #Get the index of the word in the new dataframe
                index = indices.get_loc(row['wordlength'])
                # Assign the occurence of that word
                wl_occ.iloc[index,wl_occ.columns.get_loc("occurence")] = row['occurence']
        
        return wl_occ
        
        
        
        
        
        
        
        
        
        
        
        