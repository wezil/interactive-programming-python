"""
RiceRocks
Intro to Interactive Programming Part 2

Author: Weikang Sun
Date: 9/22/15

Browser: Chrome 45.0 on Windows 8.1

CodeSkulptor source:
http://www.codeskulptor.org/#user40_CO90x2lzFs_27.py
"""

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
player_keys = [0, 0, 0, 0] # [left, right, thrust, missile]
KEYS = (simplegui.KEY_MAP['left'],
        simplegui.KEY_MAP['right'],
        simplegui.KEY_MAP['up'],
        simplegui.KEY_MAP['space'])
ANG_MULTIPLIER = 0.1
MOMENTUM_FACTOR = 2.5
rotation_normal = True
ACCELERATION = 0.3
DRAG_COEFF = 0.03
# helper tuple to draw five objects so that things properly wrap around screen
WRAP_AROUND = ([0, 0],
               [WIDTH, 0], [-WIDTH, 0],
               [0, HEIGHT], [0, -HEIGHT])
MISSILE_MULTIPLIER = 3

rock_group = set()
missile_group = set()
explosion_group = set()
god_mode = False
died = False
died_timer = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(0.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def add_vector(vector, increment, mod = False, bounds = (0, 0)):
    """ 
    Adds two 2D vectors and returns the result
    can also do modular arithmitic for wrapping
    """
    result = [0, 0]
    result[0] = vector[0] + increment[0]
    result[1] = vector[1] + increment[1]
    
    if mod:
        result[0] = result[0] % bounds[0]
        result[1] = result[1] % bounds[1]
        
    return result

def mult_vector(vector, coeff):
    """ multiplies a 2D vector by a coefficient """
    return [coeff * element for element in vector]
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = list(info.get_size())
        self.radius = info.get_radius()
        self.info = info
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_angle(self):
        return self.angle
    
    def get_angle_vel(self):
        return self.angle_vel
        
    def draw(self,canvas):
        # this loop makes the wrap around look nicer
        for wrapper in WRAP_AROUND:            
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              add_vector(self.pos, wrapper), self.image_size, self.angle)
    
    def thrust_update(self):
        if self.thrust:
            ship_thrust_sound.play()
            self.image_center[0] = self.info.get_center()[0] + self.info.get_size()[0]
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            self.image_center[0] = self.info.get_center()[0]

    def update(self):
        if rotation_normal:
            self.angle_vel = player_keys[1] - player_keys[0]
            self.angle_vel *= ANG_MULTIPLIER
        else:
            self.angle_vel += ANG_MULTIPLIER ** MOMENTUM_FACTOR * \
            (player_keys[1] - player_keys[0])
    
        self.angle += self.angle_vel
        
        self.thrust_update()
        
        if self.thrust:
            accel = mult_vector(angle_to_vector(self.angle), ACCELERATION)
            self.vel = add_vector(self.vel, accel)
        
        self.vel = mult_vector(self.vel, 1 - DRAG_COEFF)                          
        self.pos = add_vector(self.pos, self.vel, True, (WIDTH, HEIGHT))
        
    def shoot(self):
        global missile_group
        
        missile_group.add(Sprite(add_vector(self.pos, mult_vector(angle_to_vector(self.angle), self.image_size[0] / 2)), 
                          add_vector(self.vel, mult_vector(angle_to_vector(self.angle), MISSILE_MULTIPLIER)),
                          self.angle, 0, missile_image, missile_info, missile_sound))
        
         
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_angle(self):
        return self.angle
    
    def get_angle_vel(self):
        return self.angle_vel
   
    def draw(self, canvas):
        for wrapper in WRAP_AROUND:
            if self.animated:
                canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age,
                                               self.image_center[1]], self.image_size,
                                  add_vector(self.pos, wrapper), self.image_size, self.angle)
            else:
                canvas.draw_image(self.image, self.image_center, self.image_size,
                                  add_vector(self.pos, wrapper), self.image_size, self.angle)
        
    def update(self):
        self.pos = add_vector(self.pos, self.vel, True, (WIDTH, HEIGHT))
        self.angle += self.angle_vel
        self.age += 1
        return self.age > self.lifespan
        
    def collide(self, other_obj):
        return dist(other_obj.get_pos(), self.pos) <= other_obj.get_radius() + self.radius

        
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()

           
def draw(canvas):
    global time, lives, score, started, rock_group, explosion_group, died, died_timer, god_mode
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if not died:
        my_ship.draw(canvas)
    else:
        if died_timer > 60 and (died_timer // 10) % 2 == 0:
            my_ship.draw(canvas)
            
    my_ship.update()
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    if group_collide(rock_group, my_ship) and not god_mode:
        lives -= 1
        died = True
        god_mode = True
        explosion_group.add(Sprite(my_ship.get_pos(), [0, 0], my_ship.get_angle(), 
                                   my_ship.get_angle_vel(), explosion_image, 
                                   explosion_info, explosion_sound))
    
    if died:
        died_timer += 1
        
    if died_timer > 180 and died:
        died = False
        god_mode = False
        died_timer = 0
    
    score += group_group_collide(missile_group, rock_group)
    
    if lives <= 0:
        started = False
        rock_group = set()
        
    draw_gui(canvas)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    

def process_sprite_group(group, canvas):
    """ updates and draws all sprites in set """
    remove = set()
    for item in set(group):
        if item.update():
            remove.add(item)
        item.draw(canvas)
    
    group.difference_update(remove)
    

def group_collide(group, other_obj):
    if died:
        return False
    
    global explosion_group
    remove = set()
    for item in set(group):
        if item.collide(other_obj):
            remove.add(item)
            
            explosion_group.add(Sprite(item.get_pos(), [0, 0], item.get_angle(), 
                                       item.get_angle_vel(), explosion_image, 
                                       explosion_info, explosion_sound))
            
    group.difference_update(remove)
    
    if len(remove) > 0:
        return True
    return False


def group_group_collide(group1, group2):
    remove = set()
    for item in set(group1):
        if group_collide(group2, item):
            remove.add(item)
            
    group1.difference_update(remove)
    return len(remove)


def draw_gui(canvas):
    """ draw the user interface """
    
    canvas.draw_text("Lives: ", (20, 20), 20, "White", "sans-serif")
    for ship in range(lives):
        canvas.draw_image(ship_image, (45, 45), (90, 90), (30 + ship * 40, 45), (40, 40), -math.pi/2.0)
    canvas.draw_text("Score: " + str(score), (WIDTH - 100, 20), 20, "White", "sans-serif")
    

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) < 12 and started:  
        # get random position not colliding with ship
        random_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        while dist(my_ship.get_pos(), random_pos) < 75:
            random_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        
        difficulty = 1 + score / 10.0
        rock_group.add(Sprite(random_pos,
                       [difficulty*(random.random() * 2 - 1.0), difficulty*(random.random() * 2 - 1.0)],
                       (random.random() * 2 - 1.0) * math.pi,
                       difficulty*((random.random() * 0.1) - 0.05),
                       asteroid_image, asteroid_info))

        
# key handlers
def keydown(key):
    for element in KEYS:
        if key == element:
            player_keys[KEYS.index(key)] = 1
    
    if player_keys[2] == 1:
        my_ship.thrust = True
        
    if player_keys[3] == 1:
        my_ship.shoot()

def keyup(key):
    for element in KEYS:
        if key == element:
            player_keys[KEYS.index(key)] = 0
            
    if player_keys[2] == 0:
        my_ship.thrust = False
            
def rotate_normal():
    global rotation_normal
    rotation_normal = True
    
def rotate_free():
    global rotation_normal
    rotation_normal = False
    
def god_off():
    global god_mode
    god_mode = False
    
def god_on():
    global god_mode
    god_mode = True
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

frame.add_label("Ship Rotation Momentum:")
frame.add_button("None", rotate_normal)
frame.add_button("Realistic", rotate_free)

frame.add_label("God Mode")
frame.add_button("Off", god_off)
frame.add_button("On", god_on)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
