#!/usr/bin/env python
'''
-----------------------------------------
  _____                                 
 /  ___|                                
 \ `--.  __ _ _ __ ___  ___  ___  _ __  
  `--. \/ _` | '_ ` _ \/ __|/ _ \| '_ \ 
 /\__/ / (_| | | | | | \__ \ (_) | | | |
 \____/ \__,_|_| |_| |_|___/\___/|_| |_|
                                        
                                        
______                _                 
|  _  \              (_)                
| | | |__ _ _ __  _____  __ _  ___ _ __ 
| | | / _` | '_ \|_  / |/ _` |/ _ \ '__|
| |/ / (_| | | | |/ /| | (_| |  __/ |   
|___/ \__,_|_| |_/___|_|\__, |\___|_|   
                         __/ |          
                        |___/           
-----------------------------------------

Hangman Game

Python 2.7.6

samsondanziger.com

-----------------------------------------

Changelog
#v3.0
Added proper command line interface with help files and parser for CLI use
Added ascii_hangman.txt file for custom ascii hangman designs
Tidied code a bit
Added acceptance for custom wordlist from a filepath

#v2.0
Added single player support
Added section to import a wordlist for computer to use
Added choices at each stage to check correctness
Tidied interface
Fixed known bugs

#v1.0
Base hangman release
Many bugs

-----------------------------------------
'''

def Hangman():
    '''
        usage: hangman_cli.py [-h] [-p PLAYERS] [-c CHANCES] [-w WORDLIST]
                      [--ascii-off]

        A simple Hangman game
        If no arguments are given it will run as singleplayer with downloaded wordlist. Ascii art will be on.

        optional arguments:
          -h, --help            show this help message and exit
          -p PLAYERS, --players PLAYERS
                                The number of players to play hangman. Can only be 1
                                or 2.
          -c CHANCES, --chances CHANCES
                                The number of chances you have to guess the word
          -w WORDLIST, --wordlist WORDLIST
                                A file path to a local wordlist from which to select
                                words. If none is given, one will be downloaded.
          --ascii-off           Switch off ascii art hangman.

    '''
    import argparse
    import os.path
    import shutil
    import urllib
    from random import choice

    parser = argparse.ArgumentParser(description="A simple Hangman game. If no arguments are given it will run as singleplayer with downloaded wordlist. Ascii art will be on.")
    parser.add_argument('-p', '--players', default=1, help='The number of players to play hangman. Can only be 1 or 2.')
    parser.add_argument('-c', '--chances', default=8, help='The number of chances you have to guess the word')
    parser.add_argument('-w', '--wordlist', help='A file path to a local wordlist from which to select words. If none is given, one will be downloaded.')
    parser.add_argument('--ascii-off', action='store_false', help='Switch off ascii art hangman.')

    args = parser.parse_args()


    def get_variables(args):
        ascii = True
        try: # Set initial variables from parsing command line.
            players = int(args.players)
            wordlist = args.wordlist
            chances = int(args.chances)
            ascii = args.ascii_off
        except ValueError: # If players or chances isn't a number, exit the program.
            print "Please enter an integer for players and chances."
            raise SystemExit
            
        if wordlist == None: # If no wordlist is given, set it as in the local directory.
            wordlist = "wordlist.txt"
        
        if os.path.isfile(wordlist) and players==1: # Look for the wordlist
            file = open(wordlist, "r").read()
            file = file.split('\r\n')
            word = choice(file)
        elif players==1: # If no wordlist is as input, download one to the local directory.
            urllib.urlretrieve("http://www.mieliestronk.com/corncob_lowercase.txt", "wordlist.txt")
            file = open("wordlist.txt", "r").read()
            file = file.split('\r\n')
            word = choice(file)
        elif players > 1: # If the game is multiplayer, ask for a word input.
            word = raw_input("Please enter a word. This will be the word that the other players attempt to guess.\n\t")
            
        return word, chances, ascii
  
    def guess_character(word, chances, guessed_char, guessed_correct): # To be run every time a character is to be guessed.
        char = raw_input(" Guess a letter: ").lower()
        if not char.isalpha() or len(char) > 1: # Either they have entered multiple letters, or not letters.
            print " Please enter ONE LETTER only.\n"
            guess_character(word, chances, ascii, guessed_char, guessed_correct)
            
        if char in guessed_char: # They have already guessed this letter.
            print " You have already guessed this letter.\n"
        elif char in word and char not in guessed_correct: # The letter is correct but hasn't yet been guessed.
            guessed_char.append(char)
            i = 0
            while word.find(char, i) != -1: # If the letter occurs multiple times, replace all occurrences.
                l = word.find(char, i)
                guessed_correct[l] = char
                i = l+1
        elif char not in word: # The letter is an incorrect guess.
            guessed_char.append(char)
            chances -= 1
        return chances, guessed_char, guessed_correct

    def guessword(guessed_correct): # Returns your word with the blanks you have guessed correctly.
        return ''.join(guessed_correct)
        
    
    word, chances, ascii = get_variables(args)
    guessed_char = []
    guessed_correct = ["-"]*len(word)
    hangman = open("ascii_hangman.txt", "r").read()[96:].split(",") # Hangman ascii art is in a file for easy editing. 
    if ascii:
        chances = len(hangman)
    
    def print_hangman(remaining_chances): # Prints each hangman depending on remaining chances.
        try:
            hangman = hangman = open("ascii_hangman.txt", "r").read()[96:].split(",")
            l = len(hangman)
            index = l - remaining_chances
            sketch = hangman[index].split('\n')
            for s in sketch:
                print s
        except IndexError:
            print
    
    win = False
    print '\n' * 100 # Scroll down a lot so next player doesn't see word.
    
    if ascii:
        print print_hangman(chances)
    print "You have " +str(chances) + " chances remaining."
    print "Guessed letters: " + ' '.join(guessed_char)
    print "Your attempt:    " + guessword(guessed_correct)
    print '\n' * 10
    
    while win==False and chances>0:
        chances, guessed_char, guessed_correct = guess_character(word, chances, guessed_char, guessed_correct)

        if ascii:
            print '\n', str(print_hangman(chances)), '\n'
            
        if word == guessword(guessed_correct): # Win
            win = True
            print "Congratulations!!!\n\n"
            break
        else: # Lose
            print "You have " +str(chances) + " chances remaining."
            print "Guessed letters: " + ' '.join(guessed_char)
            print "Your attempt:    " + guessword(guessed_correct)
            print '\n' * 10
            
    if win == False: # To print at the end if you lost.
        print "You didn't win. Better luck next time."
        print "The word was: " + word + '\n'
    elif win == True: # To print at the end if you won.
        print "Well done, you have won the game"
        print "The word is " + ''.join(guessed_correct) + '\n'
       

Hangman() # Call the game.
            
            

