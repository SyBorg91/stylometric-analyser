# -*- coding: utf-8 -*-
"""
Created on         : 19/05/2018
Last modified on   : 27/05/2018
Author             : Satyabrat Borgohain
Description :
    
    This class is used for tokenising the input text provided from a file. It 
    also returns the number of tokens of a particular file after its 
    tokenisation.

    Objects of this class can be created for standalone puposes.
"""



class Preprocessor:
    """A preprocessor class used for tokenisation.
    
    """
    
    def __init__(self):
        """Initializes a preprocessor object, a list used for storing the tokens.
        
        """
     
        #Instance variable - a list to hold the tokens
        self.tokens = []
    
    
    def __str__(self):
        """Prints the tokenised list as a formatted string.
    
        Returns:
            The list as a formatted string.
    
        """

        prefix = 'Total number of tokens : \n' + "======================\n"
        suffix = "\n======================"
        return prefix + str(len(self.tokens)) + suffix
    
    
    def tokenise(self, input_sequence):
        """Tokenise the inputted text
    
        Function for tokenising the given input_sequence into individual tokens 
        for further analysis.
    
        Arguments:
            input_sequence (string): Text provided
    
        """
        
        #Splitting the individual tokens
        self.tokens = input_sequence.split(' ')
        
        
    def get_tokenised_list(self):
        """Getter for fetching the tokenised list
    
        Function for getting the tokenised list.
    
        Returns:
            tokens (list): A list of tokens.
    
        """

        return self.tokens
