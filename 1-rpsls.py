"""
Rock-paper-scissors-lizard-Spock game template

Author: Weikang Sun
Date: 6/1/15

Codeskulptor source:
http://www.codeskulptor.org/#user40_skVY0RD22D_2.py

"""

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

import random

INDEX_NAMES = ["rock", "Spock", "paper", "lizard", "scissors"]

def name_to_number(name):
    """
    returns the corresponding index for the thrown name
    """
    
    try:
        return INDEX_NAMES.index(name)
    except ValueError:
        print "Error: not found"
        
    # Traditional code
#    if name == "rock":
#        return 0
#    elif name == "Spock":
#        return 1
#    elif name == "paper":
#        return 2
#    elif name == "lizard":
#        return 3
#    elif name == "scissors":
#        return 4
#    else:
#        print "Error: not found"
        

def number_to_name(number):
    """
    returns the name for the corresponding index
    """
    
    try:
        return INDEX_NAMES[number]
    except IndexError:
        print "Error: invalid index"
    
    # Traditional code
#    if number == 0:
#        return "rock"
#    elif number == 1:
#        return "Spock"
#    elif number == 2:
#        return "paper"
#    elif number == 3:
#		 return "lizard"
#	 elif number == 4:
#        return "scissors"
#    else:
#        print "Error: invalid index"
        
    
def rpsls(player_choice): 
    """
    plays a single game of RPSLS given a player choice
    and a random computer choice
    """
    
    print "Player chooses", player_choice
    player_num = name_to_number(player_choice)
    
    # computes computer's random choice
    comp_num = random.randrange(0, 5)
    print "Computer chooses", number_to_name(comp_num)
    
    result_num = (comp_num - player_num) % 5
    
    if result_num == 0:
        print "Player and computer tie!"
    elif result_num < 3:
        print "Computer wins!"
    else:
        print "Player wins!"
    
    # blank line to separate games
    print


    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
