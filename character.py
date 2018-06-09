# -*- coding: utf-8 -*-
"""
Created on         : 19/5/2018
Last modified on   : 27/5/2018
Author             : Satyabrat Borgohain
Description :
    
    This class creates objects for analysing occurrence of characters in a 
    tokenised list. Characters include alphabets, numerals and punctuations.

    Objects of this class can be created for standalone puposes.
"""



import string
import pandas as pd
from collections import Counter

class CharacterAnalyser:
    """A analyser class for analysing tokenised input at the 'character' level.
    
    """
    
    #Class variable for storing all the characters to be analysed
    characters = list(string.ascii_uppercase+string.digits+string.punctuation)
    
    def __init__(self):
        """Initializes a CharacterAnalyser object which is a pandas DataFrame 
        with two columns as : 'character' which contains the characters and 
        'occurrence' which holds its corresponding occurrence in the tokenised list.
        
        """
        
        #Instance variable for storing the occurences of corresponding characters
        self.char_occ = pd.DataFrame({'character': self.characters,
                                    'occurence': [0]*len(self.characters)})

        
    def __str__(self):
        """Prints the character occurrences as a formatted string.
    
        Returns:
            The character occurence dataframe as a formatted string.
    
        """
        
        prefix = 'Character occurences : \n' + "======================\n"
        suffix = "\n======================"
        return prefix + self.char_occ.to_string(index=False, justify='left') + suffix
    
        
    def analyse_characters(self, tokenised_list):
        """Analyses the tokenised list for character occurrence.
    
        Function for analysing the given tokenised list and record the number of
        times a character has appeared in the tokens. It records the occurrences
        in the instance variable.

        Arguments:
            tokenised_list (list): The list of tokens.
    
        """
        
        #Finding the character count in the tokenised list
        char_count=Counter(''.join(tokenised_list).upper())
        
        #Updating the instance variable with the character occurrences
        for key, value in char_count.items():
            #Finding the row index with containing the particular character
            indices = pd.Index(self.characters)
            index = indices.get_loc(key)
            self.char_occ.iloc[index,1] = value


    def get_punctuation_frequency(self):
        """Getter for extracting only the punctuation occurrences in a tokenised
        list from the instance variable.
    
        Function for analysing the tokenised list and returning the occurrence
        of only the punctuations contained in it.
    
        Returns:
            punc_occ (pandas DataFrame): The dataframe of punctuation occurrrence.
    
        """
        
        punctuations = list(string.punctuation)
        #Dataframe to store the punctuation occurences only
        punc_occ = pd.DataFrame(columns=['punctuation', 'occurence'])
        #Loop for identifying rows with punctuations in the instance variable
        for i, row in self.char_occ.iterrows():
            if row['character'] in punctuations:
                temp_df = pd.DataFrame([[row['character'],row['occurence']]], 
                                       columns=['punctuation', 'occurence'])
                punc_occ = punc_occ.append(temp_df, ignore_index=True)
        
        return punc_occ
    