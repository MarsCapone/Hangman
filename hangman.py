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



word = ''
chances = 0
guessed_correct = []
guessed_char = []
name = ''
ascii = False
players = 1

HANGMAN = ['''
 _______
|   |  \|
        |
        |
        |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
        |
        |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
    |   |
        |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
   \|   |
        |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
   \|/  |
        |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
   \|/  |
    |   |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
   \|/  |
    |   |
   /    |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
   \|/  |
    |   |
   / \  |
        |
        |
       ---''']

def get_word(): # get a word
    global word
    word = raw_input("%s, please enter a word: "%name).lower()
    if not word.isalpha(): # check the word contains only letters
        print "Please enter only letters."
        get_word() # restart if not
    

def get_chances(): # get the number of chances allowed
    global chances
    global ascii
    chances = raw_input("Enter the number of chances allowed (default 5) \n Enter 0 for ASCII art hangman:   ").lower()
    try:
        if chances == '': # default 5 chances
            chances = 5
        elif int(chances)%1 == 0 and int(chances) != 0: # check if it is a number
            chances = int(chances)
        elif int(chances) == 0:
            chances = 8
            ascii = True
        elif chances.isalpha(): # if it contains letters, ask again.
            print "Please enter a NUMBER."
            get_chances()
            print
        else: # if there was some other value, start again.
            print "There has been an error."
            get_chances()
            print
    except ValueError:
        print
    

def get_name(): # get the name of the person setting the word
    global name
    name = raw_input("What is your name? ")
    c = raw_input("Is this correct? %s (y/n): "%name).lower() # check the name is correct
    if c == 'n':
        get_name()
        print

def get_players(): # choose whether to play single player or not
    global players
    print " 1. Single player    Computer chooses a word."
    print " 2. Two player       Player 1 chooses a word, player 2 guesses."
    players = input("Enter the number corresponding to your choice: ")
    if players == 1:
        print "You have selected single player, is this correct? (y/n) "
        check = raw_input().lower()
    elif players == 2:
        print "You have selected two player, is this correct? (y/n) "
        check = raw_input().lower() 
    if check == 'n':
        get_players()

def get_words(): # download word list if you don't have a wordlist already.
    import urllib
    from random import choice
    try:
        file = open('wordlist.txt', 'r').read() # check if the wordlist exists, if it does, use it.
    except IOError:
        choose = raw_input(""" Would you like to choose a wordlist file?
        If so, please enter the name of the file. It must be in the same folder as this program.
        If you would like this program to fetch a list of words, press enter.
        """) # if the wordlist doesn't exist, ask for an input wordlist, or fetch one to the same folder.
        if choose == '':
            file = urllib.urlretrieve('http://www.mieliestronk.com/corncob_lowercase.txt', 'wordlist.txt')
            file = open('wordlist.txt','r').read()
        else:
            found = False
            while not found:
                try:
                    with open(choose, 'r'): 
                        found = True
                        file = open(choose, 'r').read()
                except IOError:
                    get_words()
    file = file.split('\n') # create a list from the text file
    return choice(file) # pick a random word from the list.
            
    
def setupgame():
    global guessed_correct
    global guessed_char
    global players
    global word
    global chances
    global ascii
    ascii = False
    get_players() # get the number of players
    print
    print
    if players == 1:
        word = get_words()[:-1] # if the computer chooses a word
        chances = 8 # you get 8 chances
        ascii = True # ascii art is on
    else:
        get_name() # get the name of player 1
        get_word() # player 1 chooses a word
        get_chances() # player 1 chooses how many chances to give player 2
    print
    guessed_char = [] # all the letters guessed
    guessed_correct = ["-"]*len(word) # all correctly guessed letters
    print "\n" * 40 # add a load of new lines, so you can't see anything previously typed.


def guess_character(): # to be run every time a character should be entered.
    try:
        global word
        global chances
        global guessed_correct
        global guessed_char
        global ascii
        global HANGMAN
        char = raw_input("Guess a letter: ").lower()
        if not char.isalpha() or len(char)>1 : # check there is only one letter, if not start again.
            print "Please enter ONE LETTER."
            guess_character()
            print
        if char in guessed_char: # check if the letter has been guessed already
            print "You have already guessed this letter."
        elif char in word and char not in guessed_correct: # this bit is for a letter that hasn't yet been guessed, but is correct
            guessed_char.append(char)
            i = 0
            while word.find(char, i) != -1: # if the letter occurs multiple times, replace all occurrences.
                l = word.find(char, i)
                guessed_correct[l] = char
                i = l+1
            if ascii:
                print
                print HANGMAN[8 - chances]
                print
        elif char not in word: # for an incorrect guess
            guessed_char.append(char)
            chances -= 1
            if ascii:
                print
                print HANGMAN[8 - chances]
                print
        print
    except IndexError:
        print

def main(): # main program
    global word
    global chances
    global guessed_correct
    global guessed_char
    global ascii
    win = False # False until you win
    setupgame() # setup a new game
    if ascii:
        print
        print HANGMAN[8 - chances]
        print
    print ''.join(guessed_correct) # initially show the length of the word
    print "You have " +str(chances) + " chances remaining."
    while chances>0 and win==False: # stop if you win or run out of chances
        guess_character()
        if word == ''.join(guessed_correct): # win
            print "Congratulations!!!"
            print
            win = True
            break
        else: # lose
            print "You have " +str(chances) + " chances remaining."
            print "Guessed letters: " + ' '.join(guessed_char)
            print "Your attempt:    " + ''.join(guessed_correct)
            print '\n' * 20
    if win == False:
        print "You didn't win. Better luck next time."
        print "The word was: " + word
        print
    elif win == True:
        print "Well done, you have won the game"
        print "The word is " + ''.join(guessed_correct)
        print
        
while True: # run forever
    main()
    print
    c = raw_input("Play again? y/n: ").lower() # check to play again
    if c == 'y':
        main()
        print
    else:
        break
