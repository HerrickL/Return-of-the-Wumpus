import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import sys
import pygame
import random
from pygame.locals import *

#globals
ROOMS_CLEARED = 0
MONEY = 0
SENSE = ""
BULLETS = 2
STARTED = False
ALIVE = True
FAR_WUMP = True
INCREMENT_TIME = 0
ROOMS = {'1':(88,150),'2':(241, 150), '3':(394,150), '4':(547,150), '5':(700,150),
         '6':(88,267), '7':(241,267), '8':(394,267), '9':(547,267), '10':(700,267),
         '11':(88,384), '12':(241,384), '13':(394,384), '14':(547,384), '15':(700,384),
         '16':(88,501), '17':(241,501), '18':(394,501), '19':(547,501), '20':(700,501),
         '21':(241,618), '22':(394,618), '23':(547,618), '24':(700,618)}
NOT_CHECKED = ROOMS
BANDITS_GONE = False
BandLoc = [0,0]
Beginning = True

#start
class ImageInfo:
    def __init__(self, center, size, radius = 0, health = None, location = None):
        self.center = center
        self.size = size
        self.radius = radius
        if health:
            self.health = health
        else:
            self.health = float('inf')
        self.location = location

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_health(self):
        return self.health

    def get_animated(self):
        return self.animated

    def get_location(self):
        return self.location

#splash image    
splash_image = simplegui.load_image('https://www.dropbox.com/s/cuf9fbwuev3psm7/wumpslashsimpy.png?dl=1')
splash_info = ImageInfo([250,150],[500,300],250)
#player image from https://openclipart.org/image/300px/svg_to_png/154069/PoliceManStickFigure.png
player_image = simplegui.load_image('https://www.dropbox.com/s/kuzg5xlasaqnmsv/PoliceManStickFigure.png?dl=1')
player_info = ImageInfo([91.5,100],[183, 200],100)
#dead image from https://openclipart.org/image/300px/svg_to_png/194108/skeleton.png
dead_image = simplegui.load_image('https://www.dropbox.com/s/6esairci8p4ep6j/skeleton.png?dl=1')
dead_info = ImageInfo([124,150],[248,300],150)
#bullet art created by Kim Lathrop and may be freely reused if credited
bullet_info = ImageInfo([5,5], [10, 10], 3)
bullet_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
#bullet sound from soundbible.com, titled "Gun Shot" and recorded by Marvin. http://soundbible.com/2004-Gun-Shot.html
shots_fired = simplegui.load_sound('https://dl.dropbox.com/s/we8fpgztrnzre2q/Gun_Shot-Marvin-1140816320.ogg')
shots_fired.set_volume(.08)
#drop bullet sound from soundbible.com, titled "Bone Breaking" and recorded by Mike Koenig http://soundbible.com/46-Bone-Breaking.html
drop_bullet = simplegui.load_sound('https://dl.dropbox.com/s/a3rse4yaze0uqik/Bone%20Breaking-SoundBible.com-1159179107.ogg')
#load bullet sound from soundbible.com, titled "22 Beretta Chamber Load" and recorded by Mike Koenig http://soundbible.com/411-22-Beretta-Chamber-Load.html
load_bullet = simplegui.load_sound('https://dl.dropbox.com/s/zkynv14ijkggscj/22%20Beretta%20Chamber%20Load-SoundBible.com-286681348.ogg')
#bandits negotiation sound from soundbible.com, titled "Zombie Gibberish" and recorded by Mike Koenig http://soundbible.com/1031-Zombie-Gibberish.html
bandits_negotiation = simplegui.load_sound('https://dl.dropbox.com/s/z4nuyv9xva4gsu7/Zombie%20Gibberish-SoundBible.com-589887278.ogg')
bandits_negotiation.set_volume(.02)
#walking_sound from soundbible.com, titled "Walking On Gravel" and recorded by Caroline Ford http://soundbible.com/1432-Walking-On-Gravel.html
walking_sound = simplegui.load_sound('https://dl.dropbox.com/s/4nmknxgprq24rx0/Walking%20On%20Gravel-SoundBible.com-2023303198.ogg')
#hole sound from soundbible.com, titled "Crumbling" and recorded by Mike Koenig http://soundbible.com/1886-Crumbling.html
hole_sound = simplegui.load_sound('https://dl.dropbox.com/s/kcasdkfhiub9by1/Crumbling-Mike_Koenig-1123041125.ogg')
#wumpus wins sound from soundbible.com. titled "Dark Laugh" and recorded by HopeinAwe http://soundbible.com/2001-Dark-Laugh.html
wumpus_wins = simplegui.load_sound('https://dl.dropbox.com/s/a4zzhps6v9rqzry/Dark_Laugh-HopeinAwe-1491150192.ogg')
#you win sound from soundbible.com, titled "Winning Triumphal Fanfare" and recorded by John Stracke http://soundbible.com/1823-Winning-Triumphal-Fanfare.html
you_win = simplegui.load_sound('https://dl.dropbox.com/s/5htz2f01yx2ywla/Short_triumphal_fanfare-John_Stracke-815794903.ogg')
#money sound from soundbible.com, titled "Metal Debris Falling" and recorded by Mike Koenig http://soundbible.com/1099-Metal-Debris-Falling.html
money_sound = simplegui.load_sound('https://dl.dropbox.com/s/xl6m0wrrh79mxj2/Metal%20Debris%20Falling-SoundBible.com-238218965.ogg')
#splashscreen sound from soundbible.com, title "Horror Ambiance" and recorded by Mike Koenig http://soundbible.com/1709-Horror-Ambiance.html
splashscreen_sound = simplegui.load_sound('https://dl.dropbox.com/s/0kez1h8wqt18cv0/Horror_Ambiance-Mike_Koenig-1992154342.ogg')
splashscreen_sound.set_volume(.3)

#initialize sprites
def start():
    global wumpus, player, hole, bandits, gold, extra_bullets, NOT_CHECKED, BANDITS_GONE, BandLoc, Beginning
    
    player.position = [88,618]
    wumpus.position = ROOMS[str(random.randint(1,24))]
    wumpus.health = 1
    hole.position = ROOMS[str(random.randint(1,24))]
    bandits.position = ROOMS[str(random.randint(1,24))]
    bandits.health = 1
    gold.position = ROOMS[str(random.randint(1,24))]
    extra_bullets.position = ROOMS[str(random.randint(1,24))]
    NOT_CHECKED = {'1':(88,150),'2':(241, 150), '3':(394,150), '4':(547,150), '5':(700,150),
         '6':(88,267), '7':(241,267), '8':(394,267), '9':(547,267), '10':(700,267),
         '11':(88,384), '12':(241,384), '13':(394,384), '14':(547,384), '15':(700,384),
         '16':(88,501), '17':(241,501), '18':(394,501), '19':(547,501), '20':(700,501),
         '21':(241,618), '22':(394,618), '23':(547,618), '24':(700,618)}
    BANDITS_GONE = False
    BandLoc = [0,0]
    Beginning = True


#helper functions
def fix_placement():
    global wumpus, hole, bandits, Beginning
    
    while wumpus.position == player.position or wumpus.position == hole.position or wumpus.position == bandits.position or wumpus.position == extra_bullets.position:
        wumpus.position = ROOMS[str(random.randint(1,24))]
                
    if Beginning:
        while hole.position == bandits.position or hole.position == gold.position or hole.position == extra_bullets.position or hole.position == wumpus.position:
            hole.position = ROOMS[str(random.randint(1,24))]   
        
        while bandits.position == gold.position or bandits.position == extra_bullets.position or bandits.position == hole.position or bandits.position == wumpus.position:
            bandits.position = ROOMS[str(random.randint(1,24))]
            
        Beginning = False

def cleared_room():
    global ROOMS_CLEARED, NOT_CHECKED
    copy_list = set([])
    for x in NOT_CHECKED:
        if NOT_CHECKED[x][0] - player.position[0] == 0:
            if NOT_CHECKED[x][1] - player.position[1] == 0:
                ROOMS_CLEARED += 1
                copy_list.add(x)
    for x in copy_list:
        NOT_CHECKED.pop(x)

def sensing():
    global SENSE, STARTED, ALIVE, player, MONEY, BULLETS
    #wumpus
    SENSE = ""

    #detect for wumpus
    if player.position[0] - wumpus.position[0] == 153 or player.position[0] - wumpus.position[0] == -153:
        if player.position[1] - wumpus.position[1] == 0:
            if wumpus.health == 1:
                SENSE += "The wumpus is near. "
    elif player.position[1] - wumpus.position[1] == 117 or player.position[1] - wumpus.position[1] == -117:
        if player.position[0] - wumpus.position[0] == 0:
            if wumpus.health == 1:
                SENSE += "The wumpus is near. "
    elif player.position[0] - wumpus.position[0] == 0:
        if player.position[1] - wumpus.position[1] == 0:
            if wumpus.health == 1:
                wumpus_wins.rewind()
                wumpus_wins.play()
                SENSE = "The wumpus ate me."
                ALIVE = False
                STARTED = False
                timer.stop()
            else:
                SENSE += "I killed the wumpus! "
                
    #detect for other: hole, extra bullet, gold, bandit
    if player.position[0] - hole.position[0] == 153 or player.position[0] - hole.position[0] == -153:
        if player.position[1] - hole.position[1] == 0:
            SENSE += "I feel a breeze. "
    elif player.position[1] - hole.position[1] == 117 or player.position[1] - hole.position[1] == -117:
        if player.position[0] - hole.position[0] == 0:
            SENSE += "I feel a breeze. "
    elif player.position[0] - hole.position[0] == 0:
        if player.position[1] - hole.position[1] == 0:
            hole_sound.rewind()
            hole_sound.play()
            SENSE += "I fell down a rabbit hole. "
            player.position = [88,618]
    
    if BANDITS_GONE == False:
        if player.position[0] - bandits.position[0] == 153 or player.position[0] - bandits.position[0] == -153:
            if player.position[1] - bandits.position[1] == 0:
                SENSE += "A bandit is near. "
        elif player.position[1] - bandits.position[1] == 117 or player.position[1] - bandits.position[1] == -117:
            if player.position[0] - bandits.position[0] == 0:  
                SENSE += "A bandit is near. "
        elif player.position[0] - bandits.position[0] == 0:
            if player.position[1] - bandits.position[1] == 0:
                if MONEY == 100:
                    MONEY = 0
                    SENSE += "Bandits took my money. "
                else:
                    shots_fired.rewind()
                    shots_fired.play()
                    SENSE = "I had no money and the bandits killed me."
                    ALIVE = False
                    STARTED = False
                    timer.stop()
    elif BANDITS_GONE == True:
        if player.position[0] - BandLoc[0] == 0:
            if player.position[1] - BandLoc[1] == 0:
                SENSE += "I killed the bandit. "

    if player.position[0] - extra_bullets.position[0] == 153 or player.position[0] - extra_bullets.position[0] == -153:
        if player.position[1] - extra_bullets.position[1] == 0:
            SENSE += "Something shiny is near. "
    elif player.position[1] - extra_bullets.position[1] == 117 or player.position[1] - extra_bullets.position[1] == -117:
        if player.position[0] - extra_bullets.position[0] == 0:
            SENSE += "Something shiny is near. "
    elif player.position[0] - extra_bullets.position[0] == 0:
        if player.position[1] - extra_bullets.position[1] == 0:
            if BULLETS < 2:
                load_bullet.play()
                SENSE += "I found an extra bullet. "
                BULLETS += 1
                extra_bullets.position = [1000,1000]
            else:
                drop_bullet.rewind()
                drop_bullet.play()
                SENSE += "I don't need this extra bullet now. "

    if player.position[0] - gold.position[0] == 153 or player.position[0] - gold.position[0] == -153:
        if player.position[1] - gold.position[1] == 0:
            SENSE += "Something shiny is near. "
    elif player.position[1] - gold.position[1] == 117 or player.position[1] - gold.position[1] == -117:
        if player.position[0] - gold.position[0] == 0:
            SENSE += "Something shiny is near. "
    elif player.position[0] - gold.position[0] == 0:
        if player.position[1] - gold.position[1] == 0:
            money_sound.play()
            SENSE += "I found money. "
            MONEY = 100
            gold.position = [1000,1000]

    #Nothing detected message
    if SENSE == "":
        SENSE = "Nothing detected."
        
    if bandits.health == 0 and wumpus.health == 0 and gold.position == [1000,1000]:
        STARTED = False
        you_win.rewind()
        you_win.play()
            
def hit():
    global SENSE, wumpus, bandits, BULLETS, NOT_CHECKED, ROOMS_CLEARED, BandLoc, BANDITS_GONE
    if a_bullet.age == 1:
        shots_fired.rewind()
        shots_fired.play()
    #can hit wumpus or bandit    
    if a_bullet.age < (a_bullet.lifespan - 1):
        if a_bullet.position[0] - wumpus.position[0] <= 5 and a_bullet.position[0] - wumpus.position[0] >= -5:
            if a_bullet.position[1] - wumpus.position[1] <= 5 and a_bullet.position[1] - wumpus.position[1] >= -5:
                if wumpus.health == 1:
                    wumpus.health = 0
                    sensing()
                elif a_bullet.position[0] - bandits.position[0] <= 5 and a_bullet.position[0] - bandits.position[0] >= -5:
                    if a_bullet.position[1] - bandits.position[1] <= 5 and a_bullet.position[1] - bandits.position[1] >= -5:
                        bandits.health = 0                
                        BANDITS_GONE = True
                        BandLoc = bandits.position
                        bandits.position = [1000,1000] 
                        sensing()
        elif a_bullet.position[0] - bandits.position[0] <= 5 and a_bullet.position[0] - bandits.position[0] >= -5:
            if a_bullet.position[1] - bandits.position[1] <= 5 and a_bullet.position[1] - bandits.position[1] >= -5:
                bandits.health = 0                
                BANDITS_GONE = True
                BandLoc = bandits.position
                bandits.position = [1000,1000] 
                sensing()
    #if wump still alive, move
    else:
        if wumpus.health == 1:
            wumpus.position = ROOMS[str(random.randint(1,24))]
            fix_placement()
            ROOMS_CLEARED = 0
            NOT_CHECKED = {'1':(88,150),'2':(241, 150), '3':(394,150), '4':(547,150), '5':(700,150),
         '6':(88,267), '7':(241,267), '8':(394,267), '9':(547,267), '10':(700,267),
         '11':(88,384), '12':(241,384), '13':(394,384), '14':(547,384), '15':(700,384),
         '16':(88,501), '17':(241,501), '18':(394,501), '19':(547,501), '20':(700,501),
         '21':(241,618), '22':(394,618), '23':(547,618), '24':(700,618)}
            cleared_room()
            sensing()
                
#formats time for timer
def format_time(INCREMENT_TIME):
    minutes = (INCREMENT_TIME//600)
    seconds = (INCREMENT_TIME //10)%60
    tensSeconds = (seconds // 10)
    oneSeconds = (seconds % 10)
    tenths = (INCREMENT_TIME % 10)    
    return str(minutes) + ":" + str(tensSeconds) + str(oneSeconds) + ":" + str(tenths)

class Person:
    def __init__(self, position, image, info):
        self.position = [position[0], position[1]]
        self.image = image
        self.info = info
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.vel = [0,0]
    
    def shoot(self):
        global BULLETS, a_bullet
        #create bullet, set lifetime
        if BULLETS > 0:
            a_bullet = ammo(player.position, player.vel, 0, 25, bullet_image, bullet_info)
            BULLETS -= 1
    
    def up(self):
        self.vel = [0, -5]
        
    def down(self):
        self.vel = [0, 5]
        
    def left(self):
        self.vel = [-7, 0]
        
    def right(self):
        self.vel = [7, 0]
       
    def draw(self, canvas):
        if ALIVE:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.position, [73.2, 80])
        else:
            canvas.draw_image(dead_image, [124,150], [248,300], self.position, [73.2, 80])
    
class boss:
    def __init__(self, position, health):
        self.position = [position[0], position[1]]
        self.health = health
        
class others:
    def __init__(self, position):
        self.position = [position[0], position[1]]
    
class ammo:
    def __init__(self, position, vel, age, lifespan, image, info):
        self.position = [position[0], position[1]]
        self.vel = [vel[0],vel[1]]
        self.age = age
        self.lifespan = lifespan
        self.image = image
        self.info = info
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
     
    def draw(self, canvas):
        if self.age < self.lifespan:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.position, self.image_size)  
    
    def update(self):
        #move
        self.position[0] += self.vel[0]
        self.position[1] += self.vel[1]
        
        #update lifespan
        self.age += 1
        
        if self.age < self.lifespan:
            hit()
        
#event handlers
def draw(canvas):
    #status bar
    canvas.draw_polygon([(0, 0), (800, 0), (800, 80), (0,80)], 1, 'White', 'lavender')
    canvas.draw_text("Rooms Cleared: " + str(ROOMS_CLEARED) + "/24", (20, 30), 20, 'darkolivegreen')
    canvas.draw_text("Money Found: " + str(MONEY), (20, 60), 20, 'darkolivegreen')
    canvas.draw_text('Sensing: ' + SENSE, (300, 30), 20, 'darkolivegreen')
    canvas.draw_text('Time in the Cave:   ' + str(format_time(INCREMENT_TIME)), (300, 60), 20, 'darkolivegreen')
    canvas.draw_text('Bullets left: ' + str(BULLETS), (600, 60), 20, 'darkolivegreen')
    
    #rooms (152/116)
    canvas.draw_polyline([(0,597),(20,597), (20, 250), (20, 100), (780,100), (780, 680), (20,680),(20,647),(0,647)], 2, 'white')
    
    canvas.draw_line((20, 216), (71, 216), 2, 'white')
    canvas.draw_line((121, 216), (223, 216), 2, 'white')
    canvas.draw_line((273, 216), (375, 216), 2, 'white')
    canvas.draw_line((425, 216), (526, 216), 2, 'white')
    canvas.draw_line((576, 216), (679, 216), 2, 'white')
    canvas.draw_line((729, 216), (780, 216), 2, 'white')
    
    
    canvas.draw_line((20, 332), (71, 332), 2, 'white')
    canvas.draw_line((121, 332), (223, 332), 2, 'white')
    canvas.draw_line((273, 332), (375, 332), 2, 'white')
    canvas.draw_line((425, 332), (526, 332), 2, 'white')
    canvas.draw_line((576, 332), (679, 332), 2, 'white')
    canvas.draw_line((729, 332), (780, 332), 2, 'white')
    
    canvas.draw_line((20, 448), (71, 448), 2, 'white')
    canvas.draw_line((121, 448), (223, 448), 2, 'white')
    canvas.draw_line((273, 448), (375, 448), 2, 'white')
    canvas.draw_line((425, 448), (526, 448), 2, 'white')
    canvas.draw_line((576, 448), (679, 448), 2, 'white')
    canvas.draw_line((729, 448), (780, 448), 2, 'white')
    
    canvas.draw_line((20, 564), (71, 564), 2, 'white')
    canvas.draw_line((121, 564), (223, 564), 2, 'white')
    canvas.draw_line((273, 564), (375, 564), 2, 'white')
    canvas.draw_line((425, 564), (526, 564), 2, 'white')
    canvas.draw_line((576, 564), (679, 564), 2, 'white')
    canvas.draw_line((729, 564), (780, 564), 2, 'white')
    
    
    #Y
    canvas.draw_line((172, 100), (172, 133), 2, 'white')
    canvas.draw_line((172, 183), (172, 249), 2, 'white')    
    canvas.draw_line((172, 299), (172, 365), 2, 'white')   
    canvas.draw_line((172, 415), (172, 481), 2, 'white')
    canvas.draw_line((172, 531), (172, 597), 2, 'white')
    canvas.draw_line((172, 647), (172, 680), 2, 'white')
    
    canvas.draw_line((324, 100), (324, 133), 2, 'white')
    canvas.draw_line((324, 183), (324, 249), 2, 'white')    
    canvas.draw_line((324, 299), (324, 365), 2, 'white')   
    canvas.draw_line((324, 415), (324, 481), 2, 'white')
    canvas.draw_line((324, 531), (324, 597), 2, 'white')
    canvas.draw_line((324, 647), (324, 680), 2, 'white')
    
    canvas.draw_line((476, 100), (476, 133), 2, 'white')
    canvas.draw_line((476, 183), (476, 249), 2, 'white')    
    canvas.draw_line((476, 299), (476, 365), 2, 'white')   
    canvas.draw_line((476, 415), (476, 481), 2, 'white')
    canvas.draw_line((476, 531), (476, 597), 2, 'white')
    canvas.draw_line((476, 647), (476, 680), 2, 'white')
    
    canvas.draw_line((628, 100), (628, 133), 2, 'white')
    canvas.draw_line((628, 183), (628, 249), 2, 'white')    
    canvas.draw_line((628, 299), (628, 365), 2, 'white')   
    canvas.draw_line((628, 415), (628, 481), 2, 'white')
    canvas.draw_line((628, 531), (628, 597), 2, 'white')
    canvas.draw_line((628, 647), (628, 680), 2, 'white')
    
    canvas.draw_text('Start', (71, 650), 25, 'Purple')
    
    #player sprite and flashlight
    canvas.draw_circle((player.position[0]+ 5, player.position[1]+ 5), 45, 1, 'lemonchiffon', 'lemonchiffon')
    player.draw(canvas)
    a_bullet.draw(canvas) 
    a_bullet.update()
    
    #draw splashscreen if not started
    if not STARTED:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [800/2,700/2], [500,300] 
                          )
        splashscreen_sound.play()
    else:
        splashscreen_sound.pause()
        splashscreen_sound.rewind()
    
#timer handler
def timer_handler():
    global INCREMENT_TIME
    if STARTED:
        timer.start()
        INCREMENT_TIME += 1
    

#key handlers
def keydown(key):
    global wumpus
    #move up
    if key == simplegui.KEY_MAP['up']:
        if STARTED:
            if player.position[1] > 215:
                walking_sound.rewind()
                walking_sound.play()
                player.position[1] -= 117
                cleared_room()
                sensing()
    #move down
    if key == simplegui.KEY_MAP['down']:
        if STARTED:
            if player.position[1] < 565:
                walking_sound.rewind()
                walking_sound.play()
                player.position[1] += 117
                cleared_room()
                sensing()
    #move left
    if key == simplegui.KEY_MAP['left']:
        if STARTED:
            if player.position[0] > 171:
                walking_sound.rewind()
                walking_sound.play()
                player.position[0] -= 153
                cleared_room()
                sensing()
    #move right
    if key == simplegui.KEY_MAP['right']:
        if STARTED:
            if player.position[0] < 629:
                walking_sound.rewind()
                walking_sound.play()
                player.position[0] += 153
                cleared_room()
                sensing()
    #shoot up
    if key == simplegui.KEY_MAP['w']:
        if STARTED:
            player.up()
            player.shoot()

    #shoot down
    if key == simplegui.KEY_MAP['s']:
        if STARTED:
            player.down()
            player.shoot()
            
    #shoot left
    if key == simplegui.KEY_MAP['a']:
        if STARTED:
            player.left()
            player.shoot()
            
    #shoot right
    if key == simplegui.KEY_MAP['d']:
        if STARTED:
            player.right()
            player.shoot() 
            
def click(pos):
    global ROOMS_CLEARED, MONEY, SENSE, BULLETS, STARTED, ALIVE, INCREMENT_TIME    
    center = (400,350)
    size = splash_info.get_size()
    splashwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    splashheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not STARTED) and splashwidth and splashheight:
        #revert to starting variables
        ROOMS_CLEARED = 0
        MONEY = 0
        SENSE = ""
        BULLETS = 2
        STARTED = True
        ALIVE = True
        INCREMENT_TIME = 0
        #reset game
        start()
        fix_placement()
        sensing()
        timer.start()
        
#initialize sprites, rooms, timer, and frame
wumpus = boss(ROOMS[str(random.randint(1,24))], 1)
player = Person([88,618],player_image, player_info)
hole = others(ROOMS[str(random.randint(1,24))])
bandits = boss(ROOMS[str(random.randint(1,24))], 1)
gold = others(ROOMS[str(random.randint(1,24))])
extra_bullets = others(ROOMS[str(random.randint(1,24))])
a_bullet = ammo([1000,1000],[0,0], 0, 0, bullet_image,bullet_info)
#sensing()
timer = simplegui.create_timer(100, timer_handler)
frame = simplegui.create_frame('Return of the Wump', 800, 700)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)

#start frame and timers
timer.start()
frame.start()
