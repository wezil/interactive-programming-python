"""
IIPP Mini-Project 2: Guess the Number

Author: Weikang Sun
Date: 6/9/15

codeskulptor source:
http://www.codeskulptor.org/#user40_9uCFBsoLw2_2.py
"""

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

secret_number = 0
max_range = 100
remaining_guesses = 0

def new_game():
    """
    Begins a new game with the specified max_range
    """
    
    global secret_number
    
    compute_max_guesses()
    secret_number = random.randrange(0, max_range)
    
    print "New Game: Range [0,", str(max_range) + ")"
    print_guesses()

def compute_max_guesses():
    """
    helper function to compute the maximum guesses based
    on the binary search algorithm
    """
    
    global remaining_guesses
    # max guesses is simply the next highest integer 
    # for the log base two of the max_range
    remaining_guesses = int(math.ceil(math.log(max_range, 2)))

def print_guesses():
    """
    simple method to print the remaining guesses
    and check if game over with no guesses left
    """
    
    if remaining_guesses == 0:
        print "You ran out of guesses!"
        print "Secret number was:", secret_number
        print
        
        new_game()
    else:
        print "Remaining Guesses:", remaining_guesses
        print
    
def range100():
    """
    button that changes the range to [0,100) and starts a new game 
    """
    
    global max_range
    max_range = 100
    new_game()

def range1000():
    """
    button that changes the range to [0,1000) and starts a new game
    """
    
    global max_range
    max_range = 1000
    new_game()
    
def input_guess(input_str):
    """
    main game logic goes here when an input is entered
    """
    
    global remaining_guesses
    
    try:
        guess = int(input_str)
        print "Guess was", int(guess)
        remaining_guesses -= 1
        
        if guess < secret_number:
            print "Go higher!"
            print_guesses()
        elif guess > secret_number:
            print "Go lower!"
            print_guesses()
        else:
            print "Correct!"
            print
            new_game()
             
    except:
        print "Enter a valid guess (integer)"
        print
    
# create frame
frame = simplegui.create_frame("Guess the Number!", 100, 300)

# register event handlers for control elements and start frame
game100 = frame.add_button("Range: [0, 100)", range100, 150)
game1000 = frame.add_button("Range: [0, 1000)", range1000, 150)
guess = frame.add_input("Guess:", input_guess, 100)

frame.start()

# call new_game 
new_game()
