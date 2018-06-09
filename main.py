# -*- coding: utf-8 -*-
"""
Created on         : 19/05/2018
Last modified on   : 27/05/2018
Author             : Satyabrat Borgohain
Description :
    
    This script has the main method which drives the flow of the whole stylometric 
    analysis combining all the classes and reading the texts for their analysis.

"""



try:
    import pandas as pd
    import requests
    import preprocessor as prpscr
    import character as char
    import word
    import visualiser as vis
except ImportError as err:
    print('IMPORT ERROR :',err, '. Please check the working directory, name or '+
          'make sure that module is imported!')
    
#Variable containing names of files to be read - can be replaced with whatever 
#tokenised files need to be analysed
works = ['Edward_II_Marlowe.tok','Hamlet_Shakespeare.tok', 'Henry_VI_Part1_Shakespeare.tok', 
         'Henry_VI_Part2_Shakespeare.tok', 'Jew_of_Malta_Marlowe.tok',
         'Richard_II_Shakespeare.tok']

def main():
    """Main method for controlling the flow of the stylometric analyser.

    Function for creating of objects for word, character, punctuation, word length
    etc analysis.= to determine the patterns of styles in different works.

    """
    
    #Column names
    colnames = ['work', 'char_freq', 'punc_freq', 'stop_freq', 'word_len_freq']
    #Initializing an empty dataframe to store all stats after analysis
    all_text_stats = pd.DataFrame(columns=colnames)
    
    #Try block
    try: 
        #-----------------------------Analysis----------------------------------
        #Main loop for doing the analysis file by file
        for work in works:
            #calling read_input function to read the content of each file
            content = read_input(work)
            
            #Creating object for preprocessor class
            pre_processor = prpscr.Preprocessor()
            pre_processor.tokenise(content)
            #Fetching the tokens
            tokens = pre_processor.get_tokenised_list()
            
            #Creating object for CharacterAnalyser class
            char_analyser = char.CharacterAnalyser()
            #Analysing at character level
            char_analyser.analyse_characters(tokens)
            #Fetching the character occurences
            ch_occ = char_analyser.char_occ
            #Fetching the punctuation occurences
            punc_occ = char_analyser.get_punctuation_frequency()
            
            #Creating object for WordAnalyser class
            word_analyser = word.WordAnalyser() 
            #Analysing at word level
            word_analyser.analyse_words(tokens)
            #Fetching the stop word occurences
            stop_occ = word_analyser.get_stopword_frequency()
            #Fetching the word length occurences
            word_len_occ = word_analyser.get_word_length_frequency()
            
            #Temporary df to store all the analysis for one text at a time
            temp_df = pd.DataFrame([[work,ch_occ, punc_occ, stop_occ, word_len_occ]],
                                  columns=colnames)
        
            all_text_stats = all_text_stats.append(temp_df, ignore_index=True)
        
        #-----------------------------Visualisation-----------------------------
        #Creating object for Visualiser class
        visualiser = vis.AnalysisVisualiser(all_text_stats)
        #Visualising punctuation frequencies in all the works
        visualiser.visualise_punctuation_frequency()
        #Visualising character frequencies in all the works
        visualiser.visualise_character_frequency()
        #Visualising stopword frequencies in all the works
        visualiser.visualise_stopword_frequency()
        #Visualising word length frequencies in all the works
        visualiser.visualise_word_length_frequency()
    
    #Catch for exceptions
    except ImportError as err:
        print('IMPORT ERROR :',err, '. Please check the working directory, name or '+
          'make sure that module is imported!')
    except TypeError as err:
        print('TYPE ERROR :', err)
    except IndexError as err:
        print('INDEX ERROR :', err)
    except ValueError as err:
        print('VALUE ERROR :', err)
    except IOError as err:
        print('INPUT ERROR :',err, '. Please check the path of the file!')
    except requests.RequestException as err:
        print('REQUEST ERROR :', err)    
    except:
        print('UNEXPECTED ERROR!')
    
    
    
def read_input(work):
    """To read the files required for the stylometric analysis.

    Function for reading files.

    Arguments:
        work (string): The name of the text to be read.
        
    Returns:
        text (string): The content of the file.

    """
    
    file = open(work, 'r')
    text = ''
    for line in file:
        text += line.replace('\n', ' ')
    file.close()
    
    return text
    
    
if __name__=='__main__':
    """Function for execution of main() on running the module
    
    """
    
    main()

