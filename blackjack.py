"""
Mini-project #6 - Blackjack

Author: Weikang Sun
Date: 7/22/15
"""

import simplegui
import random
import time

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
PLAYER = False
DEALER = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        """ new hand has no cards """
        
        self._hand = []

    def __str__(self):
        """ string representation of hand """
        
        string = "Hand: "
        for card in self._hand:
            string += str(card) + " "
        return string

    def add_card(self, card):
        """ add a new card to the deck """
        
        self._hand.append(card)

    def get_value(self):
        """ get the value of the deck. A = 1 unless adding 10 will not bust """
        
        value = 0
        aces = False
        
        # sum up initial card values with A = 1
        for card in self._hand:
            value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                aces = True
                   
        # perform Ace add 10 check
        if aces and value + 10 <= 21:
            value += 10
                
        return value
   
    def draw(self, canvas, pos, is_dealer):
        """ draw a hand on the canvas, using the draw method in Card """
        
        for card in self._hand:
            # hole card is hidden until not in_play
            if self._hand.index(card) == 0 and is_dealer and in_play:
                canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, 
                                  [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            else:
                card.draw(canvas, (pos[0] + self._hand.index(card) * CARD_SIZE[0] / 2, 
                                   pos[1] + self._hand.index(card) * 5))
 
        
# define deck class 
class Deck:
    def __init__(self):
        """ full deck, not shuffled """
        
        self._deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """ shuffle the deck """
        
        random.shuffle(self._deck)

    def deal_card(self):
        """ deal a card, removing it from deck """
        
        return self._deck.pop()
    
    def __str__(self):
        """ string representation of deck """
        
        string = "Deck: "
        for card in self._deck:
            string += str(card) + " "
        return string


# initialize the deck and two hands 
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()    
    
#define event handlers for buttons
def deal():
    """ handler to start a new deck and deal """
    
    global outcome, in_play, deck, player_hand, dealer_hand, outcome, score
    
    if in_play:
        outcome = "Dealt again. Hit or Stand?"
        score -= 1
    else:
        outcome = "Hit or Stand?"
    # new deck each time (so wasteful!)
    deck = Deck()
    deck.shuffle()
    # new hands
    player_hand = Hand()
    dealer_hand = Hand()

    for dummy_idx in range(2): 
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

    in_play = True

def hit():
    """ handler to hit player hand and check busted """
    
    global score, in_play, outcome
    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    else: 
        outcome = "Hand not in play. Deal again?"
        return
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        in_play = False
        score -= 1
        outcome = "You have busted! Deal again?"
    
def stand():
    global score, in_play, outcome
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        outcome = "Standing...Dealer's turn"
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        in_play = False
    else:
        outcome = "Hand not in play. Deal again?"
        return
    
    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() > 21:
        outcome = "Dealer busts! Deal again?"
        score += 1
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "Dealer wins! Deal again?"
        score -= 1
    else:
        outcome = "You Win! Deal again?"
        score += 1  

        
# draw handler    
def draw(canvas):
    """ draw stuff on canvas """
    
    canvas.draw_text("Blackjack (Basic)", (20, 50), 40, "Black", "serif")
    canvas.draw_text(outcome, (200, 500), 30, "Black", "serif")
    canvas.draw_text("Score: " + str(score), (450, 50), 30, "Black", "serif")
    canvas.draw_text("Your hand value: " + str(player_hand.get_value()),
                     (200, 280), 20, "Black", "serif")
    
    player_hand.draw(canvas, (200, 300), PLAYER)
    dealer_hand.draw(canvas, (200, 100), DEALER)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

