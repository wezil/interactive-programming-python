"""
Memory Card Game
IIPP Part 2

Author: Weikang Sun
Date: 7/13/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_qKzEGCTI6Z_9.py
"""

import simplegui
import random

# global variables
cards_list = []
exposed = []
state = 0
selected_cards = []
turns = 0
game_over = False


def new_game():
    """itialize global variables"""
    
    global cards_list, exposed, state, selected_cards, turns, game_over
    
    # create list of double cards [0-8) 
    cards_list = range(8)
    cards_list.extend(range(8))
    random.shuffle(cards_list)
    
    # set new exposed list to all False
    exposed = [False for dummy_idx in range(16)]
    
    # set game state
    state = 0
    selected_cards = []
    turns = 0
    label.set_text("Turns = 0")
    game_over = False

     
# define event handlers
def mouseclick(pos):
    """mouse click logic here"""
    
    global state, selected_cards, turns, game_over
    
    # determine index from click position
    index = int(pos[0] / 50)
    
    # second part of statement checks if user clicks two unmatching cards
    # and then clicks on one of those cards again
    if not exposed[index] or (state == 2 and index in selected_cards):
        selected_cards.append(index)
    
        # change game state
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
            turns += 1
            label.set_text("Turns = " + str(turns))
        else:
            state = 1
            
            # check if selected cards  match or not
            index1 = selected_cards.pop(1)
            index0 = selected_cards.pop(0)
            
            if cards_list[index1] != cards_list[index0]:
                exposed[index1] = False
                exposed[index0] = False
                
        exposed[index] = True
        
        # check game over
        if not False in exposed:
            game_over = True
                
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    """draw cards and stuff on canvas"""

    for index in range(len(cards_list)):
        # draw card numbers on canvas
        if exposed[index]:
            canvas.draw_polygon([(index * 50, 0), (50 + index * 50, 0),
                                 (50 + index * 50, 100), (index * 50, 100)],
                                2, "Gray", "Black")
            canvas.draw_text(str(cards_list[index]), (5 + index * 50, 75),
                        75, "White", "serif")
                
        # draw card back if not exposed
        else:
            canvas.draw_polygon([(index * 50, 0), (50 + index * 50, 0),
                                 (50 + index * 50, 100), (index * 50, 100)],
                                2, "White", "Green")

        if not game_over:    
            # draw the selection number
            for idx in selected_cards:
                canvas.draw_text("(" + str(selected_cards.index(idx) + 1) + ")",
                                 (5 + idx * 50, 95), 14, "White", "serif")
        else:
            canvas.draw_polygon([(210, 15), (590, 15), (590, 85), (210, 85)],
                            2, "White", "Green")
            canvas.draw_text("Game Over!", (215, 75), 75, "White", "serif")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
