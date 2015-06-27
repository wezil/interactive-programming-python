"""
The most ridiculous implementation
of Pong you will see on CodeSkulptor

NOTE: may consume a lot of memory on your computer
try restarting the game or app once in a while

NOTE 2: In order to experience the full game
please make sure to have Quicktime or a supporting
audio device enabled on your browser!

Note 3: To stop the soundtrack from playing,
press the Reset button (left-arrow) at the top of this window

MULTI PLAYER  = two players (W/S for player 1, UP/DOWN for player 2)
SINGLE PLAYER = one player (UP/DOWN)

AI (can only select in SINGLE PLAYER):
MONKEY     = dumb AI, mostly goes towards the ball
HUMAN      = follows ball rigorously on own side
TERMINATOR = predicts ball trajectory

I'M GOOD AT PONG = normal pong physics
I'M A BOSS       = introduces ball spin with moving paddle 
                   (spin is not super accurate on walls)
     
RESTART GAME = should be obvious 
PLAY/PAUSE   = you get the idea
GOD MODE     = single player is invincible

Author: Weikang Sun
Date 6/26

CodeSkulptor source:
http://www.codeskulptor.org/#user40_pZgVJntu9RrQx3h.py
"""

# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

canvas_color = "green"
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
ball_spin = 0.0

# center of the paddle position
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - 1 - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
# paddle should reach one from side to the other in 1 second
PADDLE_VEL = HEIGHT / 60.0
# check which keys have been pressed [UP, DOWN] for better paddle handling
paddle1_keys = [0, 0]
paddle2_keys = [0, 0]
paddle_color = "white"

score1 = score2 = 0
game_paused = True

cpu_playing = False
cpu_difficulty = "human"
# global variable for CPU prediction
has_predicted = False
predicted_target = 0
ahnold_jargon = []

game_variation = "Normal"

# debug condition to enable god mode
DEBUG = False

# CPU lose sounds
# WHO ARE YOU
URL_SOUNDS_LOSE = ["http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/collateral_damage/collateral_damage_no.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movie_stars/schwarzenegger/mother_talk.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/kindergarten_cop/stop_it.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movie_stars/schwarzenegger/sob.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movie_stars/schwarzenegger/fist.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t3_dont_do_dat.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/total_recall/who_are_you.wav",
                   "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t1_be_back.wav"]
# CPU win sounds
# HASTA LA VISTA BABY
URL_SOUNDS_WIN = ["http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/kindergarten_cop/daddy.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/kindergarten_cop/lack_discipline.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/kindergarten_cop/stop_whining_x.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movie_stars/schwarzenegger/police.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movie_stars/schwarzenegger/whats_the_matter.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t1_excellent.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t2_hasta_la_vista.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t2_no_problemo.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t1_get_out.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t1_clothes_x.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t3_hand.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t3_terminated.wav",
                  "http://www.wavsource.com/snds_2015-06-21_1242597539702378/movies/terminator/t3_destiny.wav"]

# theme from terminator 2
# IT IS INEVITABLE
terminator_theme = simplegui.load_sound("http://www.tctwente.com/wp-admin/Vloermuziek/TCT-terminator.mp3")
terminator_theme.set_volume(0.4)
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """
    creates a new ball going in the direction specified
    """
    global ball_pos, ball_vel, ball_spin, has_predicted

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    vel_modifier = 1
    if direction == LEFT:
        vel_modifier = -1
    
    ball_vel = [random.randrange(120, 240) * vel_modifier / 60.0,
                random.randrange(60, 180) / -60.0]
    
    ball_spin = 0.0
    
    has_predicted = False
    
# define event handlers
def new_game():
    """
    resets everything and starts a new game
    """
    
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global game_paused

    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - 1 - HALF_PAD_WIDTH, HEIGHT / 2]
    
    score1 = score2 = 0
    
    spawn_ball(RIGHT)
    
    game_paused = True

def update_ball():
    """
    updates ball position and velocity
    checks ball collision and scoring ball play
    """
    
    global score1, score2, has_predicted, ball_spin
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # ball spin analyzer which affects velocity
    if game_variation == "Expert" and ball_spin != 0.0:
        update_ball_spin()
        
    # prevent ball horizontal velocity from being too low
    if abs(ball_vel[0]) < 0.5:
        ball_vel[0] *= 2
        
    # ball collision with left paddle detection
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and ball_vel[0] < 0:
        # the extra radius / sqrt(2) addition factor helps make the 
        # paddle bounce more forgiving and slightly more realistic
        if abs(ball_pos[1] - paddle1_pos[1]) <= HALF_PAD_HEIGHT + BALL_RADIUS / math.sqrt(2):
            ball_vel[0] *= -1.1 # velocity multiplier
            ball_vel[1] *= 1.1
                
            # ball spin in expert mode    
            if game_variation == "Expert":
                ball_spin = float(paddle1_vel)
            
            has_predicted = False
            
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
            # play ahnold losing sound
            # YOU SON OF A BITCH
            if cpu_playing and cpu_difficulty == "TERMINATOR":
                sound = simplegui.load_sound(random.choice(URL_SOUNDS_LOSE))
                sound.set_volume(0.5)
                sound.play()
    
    # ball collision with right paddle detection
    elif ball_pos[0] >= (WIDTH - 1 - PAD_WIDTH) - BALL_RADIUS and ball_vel[0] > 0:
        if DEBUG or abs(ball_pos[1] - paddle2_pos[1]) <= HALF_PAD_HEIGHT + BALL_RADIUS / math.sqrt(2):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
                
            if game_variation == "Expert":
                ball_spin = float(-paddle2_vel)
                                              
            has_predicted = False
            
        else:
            spawn_ball(LEFT)
            score1 += 1
            
            # play ahnold winning sound
            # WHO IS YOUR DADDY?
            if cpu_playing and cpu_difficulty == "TERMINATOR":
                sound = simplegui.load_sound(random.choice(URL_SOUNDS_WIN))
                sound.set_volume(0.5)
                sound.play()
    
    # wall collision detection         
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] *= -1
        ball_pos[1] = max(min(ball_pos[1], HEIGHT - 1 - BALL_RADIUS), BALL_RADIUS)
   
def update_ball_spin():
    """
    method to change velocity based on ball spin 
    """
    
    global ball_spin
    
    # calculates a vector perpendicular to the velocity
    # and modifies the velocity by scaled spin amount
    ball_vel[0] += ball_spin / PADDLE_VEL / 15 * ball_vel[1]
    ball_vel[1] -= ball_spin / PADDLE_VEL / 15 * ball_vel[0]
    
    # reduces ball spin every time, to 0.0 if less than 0.01
    ball_spin = ball_spin / 1.05
    if abs(ball_spin) < 0.01:
        ball_spin = 0.0
    
def update_paddles():
    """
    updates paddle position with paddle velocity
    updates paddle velocity with paddle key manager
    prevents paddles from leaving screen
    """
    
    global paddle1_vel, paddle2_vel
    
    # update paddle positions
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    # update paddle velocities given key map  
    if not cpu_playing:
        paddle1_vel = (paddle1_keys[0] + paddle1_keys[1]) * PADDLE_VEL
    paddle2_vel = (paddle2_keys[0] + paddle2_keys[1]) * PADDLE_VEL
    
    # paddle 1 collision detection
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
        # this reset is necessary to prevent impossible spin
        # when the paddle is at one of the sides and a player
        # is holding down the key to move into the wall
        paddle1_keys[0] = 0
    elif paddle1_pos[1] > (HEIGHT - 1) - HALF_PAD_HEIGHT:
        paddle1_pos[1] = (HEIGHT - 1) - HALF_PAD_HEIGHT
        paddle1_keys[1] = 0
    
    # paddle 2 collision detection
    if paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
        paddle2_keys[0] = 0
    elif paddle2_pos[1] > (HEIGHT - 1) - HALF_PAD_HEIGHT:
        paddle2_pos[1] = (HEIGHT - 1) - HALF_PAD_HEIGHT
        paddle2_keys[1] = 0

def paddle_coord(paddle):
    """
    helper function to get four coordinates of paddle
    to draw a rectangle
    
    returns a list of tuples
    """
    paddle_coords = []
    
    paddle_coords.append((paddle[0] - HALF_PAD_WIDTH, paddle[1] - HALF_PAD_HEIGHT))
    paddle_coords.append((paddle[0] + HALF_PAD_WIDTH, paddle[1] - HALF_PAD_HEIGHT))
    paddle_coords.append((paddle[0] + HALF_PAD_WIDTH, paddle[1] + HALF_PAD_HEIGHT))
    paddle_coords.append((paddle[0] - HALF_PAD_WIDTH, paddle[1] + HALF_PAD_HEIGHT))
    
    return paddle_coords

def pause():
    """
    pause and unpause the game
    """
    global game_paused
    game_paused = not game_paused
    
def computer_play():
    """
    controls the CPU paddle
    """
    
    global paddle1_vel, has_predicted, predicted_target
    
    # monkey moves the paddle sometimes towards the ball
    if cpu_difficulty == "monkey":
        choice = random.randrange(10)
        if choice == 0:
            if ball_pos[1] < paddle1_pos[1]:
                paddle1_vel = -PADDLE_VEL
            else:    
                paddle1_vel = PADDLE_VEL
        elif choice == 9:
           paddle1_vel = 0
    
    # human tracks the ball once it's on the CPU side      
    elif cpu_difficulty == "human":
        if ball_pos[0] < WIDTH / 2 and ball_vel[0] < 0:
            distance = ball_pos[1] - paddle1_pos[1]
            
            if distance < 0:
                paddle1_vel = max(-PADDLE_VEL, distance)
            elif distance > 0:
                paddle1_vel = min(PADDLE_VEL, distance)
            else:
                paddle1_vel = 0
        else:
            paddle1_vel = 0
    
    # TERMINATOR predicts the path of the ball in play
    elif cpu_difficulty == "TERMINATOR":
        # checks if the ball is spinning, must predict path if it is
        if ball_spin != 0.0:
            has_predicted = False
        
        # get target trajectory once
        if not has_predicted:
            predicted_target = calculate_trajectory()
            has_predicted = True
        
        # iterate until paddle is at target
        predicted_distance = predicted_target - paddle1_pos[1]
        if predicted_distance < 0:
            paddle1_vel = max(-PADDLE_VEL, predicted_distance)
        elif predicted_distance > 0:
            paddle1_vel = min(PADDLE_VEL, predicted_distance)
        else:
            paddle1_vel = 0
        
        if not game_paused:
            update_ahnold_jargon()
        
def calculate_trajectory():
    """
    method that CPU can use to predict ball trajectory
    
    returns the predicted y-height for paddle to go in 
    order to intercept ball
    """
    
    # make a copy of all ball parameters
    ball_pos_copy = list(ball_pos)
    ball_vel_copy = list(ball_vel)
    ball_spin_copy = ball_spin
    
    # iterate ball for projected trajectory
    while (ball_pos_copy[0] > PAD_WIDTH + BALL_RADIUS or ball_vel_copy[0] > 0):
        
        ball_pos_copy[0] += ball_vel_copy[0]
        ball_pos_copy[1] += ball_vel_copy[1]
        
        # predict wall and return paddle bounce
        if ball_pos_copy[0] >= (WIDTH - 1 - PAD_WIDTH) - BALL_RADIUS:
            ball_vel_copy[0] *= -1.1
            ball_vel_copy[1] *= 1.1
        if ball_pos_copy[1] <= BALL_RADIUS or ball_pos_copy[1] >= (HEIGHT - 1) - BALL_RADIUS:
            ball_vel_copy[1] *= -1
            
        if abs(ball_vel_copy[0]) < 0.5:
            ball_vel_copy[0] *= 2
        
        # predict ball spin
        ball_vel_copy[0] += ball_spin_copy / PADDLE_VEL / 15 * ball_vel_copy[1]
        ball_vel_copy[1] -= ball_spin_copy / PADDLE_VEL / 15 * ball_vel_copy[0]
    
        ball_spin_copy = ball_spin_copy / 1.05
        if abs(ball_spin_copy) < 0.01:
            ball_spin_copy = 0.0
    
    # should return a value where the center of paddle can reach
    return min(max(HALF_PAD_HEIGHT, ball_pos_copy[1]), HEIGHT - 1 - HALF_PAD_HEIGHT)
 
def update_ahnold_jargon():
    """
    method to update jibberish terminator stuff on screen.
    GET TO DA CHOPPA
    """
    
    global ahnold_jargon
    
    ahnold_jargon.append((random.randrange(1000000000) * 
                          random.randrange(1000000000) * 
                          random.randrange(1000000000) * 
                          random.randrange(1000000000)) % 
                         1000000000000000000000000000000)
    
    if len(ahnold_jargon) > 10:
        ahnold_jargon = ahnold_jargon[1:]
    
def draw(canvas):
    """
    draws stuff
    """
    
    frame.set_canvas_background(canvas_color)
      
    # draws ahnold jargon
    # WHO'S YO DADDY
    if cpu_playing and cpu_difficulty == "TERMINATOR":
        for counter in range(len(ahnold_jargon)):
            #canvas.draw_text(str(ahnold_jargon[counter]), (10, paddle1_pos[1] - 35 + 8 * counter),
            #                 8, "gray", "monospace")
            canvas.draw_text(str(ahnold_jargon[counter]), (30, 80 + 30 * counter),
                             30, "gray", "monospace")
            
        if game_paused:
            terminator_theme.pause()
        else:
            terminator_theme.play()
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")       
    
    # update ball and paddles
    if not game_paused:
        update_paddles()
        update_ball()
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "black", "white")

    # draw paddles with the help of a helper function
    canvas.draw_polygon(paddle_coord(paddle1_pos), 1, "black", paddle_color)
    canvas.draw_polygon(paddle_coord(paddle2_pos), 1, "black", paddle_color) 

    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 2 - 55 - 25 * len(str(score1)), 50),
                     50, "black", "sans-serif")
    canvas.draw_text(str(score2), (WIDTH / 2 + 50, 50),
                     50, "black", "sans-serif")
    
    # draw player/computer indicator
    canvas.draw_text("Player", (WIDTH - 60, 20), 14, "white", "sans-serif")
    paddle1_label = "Player"
    if cpu_playing:
        paddle1_label = "CPU"
    canvas.draw_text(paddle1_label, (20, 20), 14, "white", "sans-serif")
    
    # draw CPU difficulty
    if cpu_playing:
        canvas.draw_text("AI: " + cpu_difficulty, (20, HEIGHT - 30),
                         14, "white", "sans-serif")
                     
    # draw pause screen text
    if game_paused:
        canvas.draw_text("Paused: Press Enter", (WIDTH / 2 - 220, HEIGHT / 2),
                         50, "black", "sans-serif") 
    
    # draw Pong variation text
    game_label = {"Normal": "Basic IIPP Pong",
                  "Intermediate": "Paddle-Dependent Reflection",
                  "Expert": "Paddle Spin!"}[game_variation]
    canvas.draw_text(game_label, (20, HEIGHT - 10),
                     14, "white", "sans-serif")
    
    # god mode draw
    if DEBUG:
        canvas.draw_polygon([(WIDTH - 1 - PAD_WIDTH, 0), (WIDTH, 0),
                            (WIDTH, HEIGHT - 1), (WIDTH - 1 - PAD_WIDTH, HEIGHT - 1)],
                            1, "black", paddle_color)
        canvas.draw_text("Invincible!", (WIDTH - 90, HEIGHT - 10),
                         14, "white", "sans-serif")
    
def keydown(key):
    """
    detects key down actions
    
    better handling of multiple key presses for paddes
    """
    global game_paused
    
    if not cpu_playing:
        if key == simplegui.KEY_MAP['w']:
            paddle1_keys[0] = -1
        elif key == simplegui.KEY_MAP['s']:
            paddle1_keys[1] = 1
    
    if key == simplegui.KEY_MAP['up']:
        paddle2_keys[0] = -1
    elif key == simplegui.KEY_MAP['down']:
        paddle2_keys[1] = 1
    elif key == 13:
        game_paused = not game_paused
   
def keyup(key):
    """
    detects key up actions
    """
    if not cpu_playing:
        if key == simplegui.KEY_MAP['w']:
            paddle1_keys[0] = 0
        elif key == simplegui.KEY_MAP['s']:
            paddle1_keys[1] = 0
        
    if key == simplegui.KEY_MAP['up']:
        paddle2_keys[0] = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_keys[1] = 0
        
def two_player():
    """
    enables two player
    """
    
    global cpu_playing, DEBUG
    cpu_playing = False
    # Turn off god mode
    DEBUG = False
    
    new_game()

def one_player():
    """
    enables single player
    """
    
    global cpu_playing
    cpu_playing = True
    
    new_game()

def monkey():
    """
    dumb computer intelligence
    """
    
    global cpu_difficulty, canvas_color
    if cpu_playing:
        cpu_difficulty = "monkey"
        canvas_color = "orange"
        terminator_theme.pause()

def human():
    """
    okay computer intelligence
    """
    
    global cpu_difficulty, canvas_color
    if cpu_playing:
        cpu_difficulty = "human"
        canvas_color = "green"
        terminator_theme.pause()

def terminator():
    """
    ridiculous computer intelligence
    """
    global cpu_difficulty, has_predicted, canvas_color
    if cpu_playing:
        cpu_difficulty = "TERMINATOR"
        has_predicted = False
        canvas_color = "red"
        
        terminator_theme.rewind()
        terminator_theme.play()

def beginner():
    """
    vanilla Pong from IIPP
    """
    
    global game_variation, paddle_color
    game_variation = "Normal"
    paddle_color = "white"
    new_game()

def expert():
    """
    enables ball spin
    """
    
    global game_variation, paddle_color
    game_variation = "Expert"
    paddle_color = "yellow"
    new_game()
    
def cpu_controller():
    """
    timer handler for CPU controller
    """
    if cpu_playing:
        computer_play() 
        
def god_mode():
    """
    turns the debug test into an invulnerable god mode
    """
    
    global DEBUG
    if cpu_playing:
        DEBUG = not DEBUG
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# frame buttons
frame.add_button("Multi Player", two_player)
frame.add_button("Single Player", one_player)

frame.add_label("")
frame.add_label("AI Difficulty")
frame.add_button("Monkey", monkey)
frame.add_button("Human", human)
frame.add_button("TERMINATOR", terminator)

frame.add_label("")
frame.add_label("Pong Variation")
frame.add_button("I'm good at Pong", beginner)
frame.add_button("I'm a BOSS", expert)

frame.add_label("")
frame.add_button("Restart Game", new_game)
frame.add_button("Pause/Resume", pause)
frame.add_button("God Mode (SP)", god_mode)

# start frame
new_game()
frame.start()

timer = simplegui.create_timer(25, cpu_controller)
timer.start()
