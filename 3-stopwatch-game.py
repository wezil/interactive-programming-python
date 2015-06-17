"""
Stopwatch: The Game
Try to stop the stopwatch on a whole second

Author: Weikang Sun
Date: 6/16/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_4jcI1JhVFY_3.py
"""

import simplegui

# time in tenths of a second
the_time = 0
success_tries = 0
total_tries = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    function to format the stopwatch time to A:BC.D
    Returns: the formatted six character string
    """
        
    A = t/600
    t = t - A * 600
    # this round function isn't needed when t is an integer
    CD = round(t/10.0, 1)
    
    B = ""
    if CD < 10.0:
        B = "0"
    
    return str(A) + ":" + str(B) + str(CD)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    """handler to start the timer"""
    
    # this check fixes the "lag" when spamming the start button
    if not timer.is_running():
        timer.start()
    
def stop_timer():
    """handler to stop the timer"""
    
    global success_tries, total_tries

    
    if timer.is_running():
        timer.stop()
        
        total_tries += 1
        if the_time % 10 is 0:
            success_tries += 1
    
def reset_timer():
    """handler to stop and reset the timer"""
    
    global the_time, success_tries, total_tries
    stop_timer()
    the_time = 0
    success_tries = 0
    total_tries = 0

def timer_handler():
    """timer handler which increments in 0.1 seconds"""
    
    global the_time
    the_time += 1

def draw_handler(canvas):
    """draws stopwatch game on canvas"""
    
    canvas.draw_text(format(the_time), [90, 100], 50, "white")
    
    canvas.draw_text(str(success_tries) + "/" + str(total_tries),
                     [10, 30], 30, "green")
    
# create frame stuffs
frame = simplegui.create_frame("Stopwatch: The Game", 300, 150)
timer = simplegui.create_timer(100, timer_handler)

frame.add_button("Start", start_timer)
frame.add_button("Stop", stop_timer)
frame.add_button("Reset", reset_timer)

frame.set_draw_handler(draw_handler)

frame.start()
