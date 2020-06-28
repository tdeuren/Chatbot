"""This is the game Snake.
There is a field surrounded by walls and a wall in the middle. 
Food is spawned random on the field. There is always one food item on the field. The color of the spawned food is the standaard color or can change with each spawn. If you catch the food item, the snake changes color in the color of the food item.
Traps spawn random on the field. There placement changes regulary.
Robbers come from the right of the screen and go to the left. They gradually go faster. Robbers can be turned off. If robbers are turned on, an item regulary appears that slows them down.
Accelerators regulary appear on the field if turned on. They accelerate the player. If the accelerators are turned on, an item regulary appears that slows the player down.
If the snake hits a wall or a trap or a robber, the game is over.
The highest score is kept and changes if a new highscore is reached.

Pygame was used for the graphics."""
import pygame
import random


# Standard settings
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
purple = (50, 40, 70)
braun = (75, 60, 30)
green = (0, 255, 0)
green2 = (75, 161, 37)
blue = (0, 0, 255)
magenta = (230, 0, 160)
lightblue = (20, 200 , 200)


# Classes
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, statecolor):
        pygame.sprite.Sprite.__init__(self)
        self.statecolor = statecolor
        self.color = green
        self.fig = 'imgs/GroeneAppel.png'
        if self.statecolor:
            self.random = int(random.randrange(0, 4))
            self.colors = [green, blue, purple, lightblue]
            self.figures = ['imgs/GroeneAppel.png', 'imgs/BlauweDruif.png', 'imgs/MagentaPruim.png', 'imgs/LichtblauweBes.png']
            self.color = self.colors[self.random]
            self.fig = self.figures[self.random]
        self.image = pygame.image.load(self.fig).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def givecolor(self):
        return self.color

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, hight):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, hight])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.walls = None
        self.end = 0
        self.dir = 1 #1 = right, 2 = left, 3 = up, 4 = down
        self.dirchange = 0
        self.speed1, self.speed2, self.speed3, self.speed4 = 0, 0, 0, 0
        self.accel = 0
        self.acceller = 0
        if self.dir == 1:
            self.speed1, self.speed2, self.speed3, self.speed4 = 3, 0, 0, 0
        elif self.dir == 2:
            self.speed1, self.speed2, self.speed3, self.speed4 = 0, 3, 0, 0
        elif self.dir == 3:
            self.speed1, self.speed2, self.speed3, self.speed4 = 0, 0, 3, 0
        elif self.dir == 4:
            self.speed1, self.speed2, self.speed3, self.speed4 = 0, 0, 0, 3
    def changedir(self, d):
        if d < 3:
            if self.dir > 2:
                self.dirchange = d
        else:
            if self.dir < 3:
                self.dirchange = d
    def givecoor(self):
        return (self.rect.x, self.rect.y)
    def givedir(self):
        return self.dir
    def accelerate(self):
        self.acceller = 1
    def slow(self):
        self.acceller = -1
    def setwalls(self, walls):
        self.walls = walls
    def update(self):
        if self.acceller != 0:
            self.accel += self.acceller
            if self.accel <= -2:
                self.accel = -1
            self.acceller = 0
        if self.dirchange > 0:
            self.dir = self.dirchange
            self.dirchange = 0
        if self.dir == 1:
            self.speed1, self.speed2, self.speed3, self.speed4 = 2 + self.accel, 0, 0, 0
        elif self.dir == 2:
            self.speed1, self.speed2, self.speed3, self.speed4 = 0, -2 - self.accel, 0, 0
        elif self.dir == 3:
            self.speed1, self.speed2, self.speed3, self.speed4 = 0, 0, -2 - self.accel, 0
        elif self.dir == 4:
            self.speed1, self.speed2, self.speed3, self.speed4 = 0, 0, 0, 2 + self.accel
        if self.speed1 != 0:
            self.rect.x += self.speed1
            hits = pygame.sprite.spritecollide(self, self.walls, False)
            if len(hits) > 0:
                self.end = 1
        elif self.speed2 != 0:
            self.rect.x += self.speed2
            hits = pygame.sprite.spritecollide(self, self.walls, False)
            if len(hits) > 0:
                self.end = 1
        elif self.speed3 != 0:
            self.rect.y += self.speed3
            hits = pygame.sprite.spritecollide(self, self.walls, False)
            if len(hits) > 0:
                self.end = 1
        elif self.speed4 != 0:
            self.rect.y += self.speed4
            hits = pygame.sprite.spritecollide(self, self.walls, False)
            if len(hits) > 0:
                self.end = 1

class Figure(pygame.sprite.Sprite):
    def __init__(self, x, y, statecolor):
        self.list = [(x,y)]
        self.lenght = 1
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.end = 0
        self.color = green
        self.colors = green
        self.figures = pygame.sprite.Group()
        for i in self.list:
            part = Part(i[0], i[1], self.color)
            self.figures.add(part)
        self.statecolor = statecolor
    def changespeed(self, x, y):
        self.change_x = x
        self.change_y = y
    def changesize(self):
        self.score = 1
    def givelist(self):
        return self.list
    def givefigures(self):
        return self.figures
    def changecolor(self, color):
        self.colors = color
    def changestatecolor(self, statecolor):
        self.statecolor = statecolor
    def update(self):
        if self.statecolor:
            self.color = self.colors
        self.list.append((self.change_x , self.change_y))
        if self.score > 0:
            self.lenght += self.score
            self.score = 0
        if len(self.list) > self.lenght:
            self.list.remove(self.list[0])
        self.figures = pygame.sprite.Group()
        for i in self.list:
            if i == self.list[-1]:
                part = Head(i[0], i[1])
            else:
                part = Part(i[0], i[1], self.color)
            self.figures.add(part)
        for i, n in enumerate(self.list):
            if n == self.list[0] and i != 0:
                self.end = 1
    
class Part(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([21, 21])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Head(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([21, 21])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/Spookje.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Robber(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/Spookje.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.slowe = 3
        self.slowd = 0
    def slow(self):
        self.slowd = -1
    def accelerate(self):
        self.slowd = 1
    def update(self):
        self.slowe += self.slowd
        self.slowd = 0
        if self.slowe < 1:
            self.slowe = 1
        self.rect.x += self.slowe
        if self.rect.x > 460:
            self.rect.x = random.randrange(-200, -2)
            self.rect.y = random.randrange(50, 480)

class Accelerator(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/Versneller.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Slower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/Slak.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class SlowerRobber(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/SpookjeTraag.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




# Game mechanics
    # Initialiazing
def init(xdisplay, ydisplay, name):
    pygame.init()
    display = pygame.display.set_mode([xdisplay, ydisplay])
    pygame.display.set_caption(name)
    return display

    # Write text
def write(font, text, color, display, place):
    txt = font.render(text, True, color)
    display.blit(txt, place)

    # Read highscore
def readhigh(name):
    with open(name, 'r') as file:
        z = file.read()
        try:
            highscore = int(z)
        except:
            highscore = 0
    return highscore

    # Improve highscore
def improvehigh(name, newhighscore, highscore, score):
    with open(name, 'w') as file:
        if score > highscore:
            file.write(str(score))
            newhighscore = True
        else:
            file.write(str(highscore))
    return newhighscore

    # Add walls
def addwalls(walls, allblocks):
    wall1 = Wall(0, 0, 10, 500)
    wall2 = Wall(0, 40, 460, 10)
    wall3 = Wall(0, 490, 460, 10)
    wall4 = Wall(450, 0, 10, 500)
    wall5 = Wall(225, 130, 10, 240)
    for i in range(1, 6):
        walls.add(eval('wall%s' %int(i)))
    for i in walls:
        allblocks.add(i)
    return walls, allblocks

    # User moves settings
def usermovessetting(done, done2, done3, staterobber, stateaccel, statecolor, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
            done2 = False
            done3 = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if staterobber:
                    staterobber = False
                else:
                    staterobber = True
            elif event.key == pygame.K_RIGHT:
                done = False
            elif event.key == pygame.K_LEFT:
                if stateaccel:
                    stateaccel = False
                else:
                    stateaccel = True
            elif event.key == pygame.K_UP:
                if statecolor:
                    statecolor = False
                else:
                    statecolor = True
            elif event.key == pygame.K_r:
                done = False
                done2 = False
                done3 = False
                play(display)
    return done, done2, done3, staterobber, stateaccel, statecolor

    # Make robbers and slowerrobbers
def makerob(staterobber, robbers, robber, allblocks, slowerrobbers, slowerrobber, walls):
    if staterobber:
        robbers = pygame.sprite.Group()
        for i in range(3):
            xrobber = random.randrange(-200, -2)
            yrobber = random.randrange(50, 480)
            robber = Robber(xrobber, yrobber)
            robbers.add(robber)
        for i in robbers:
            allblocks.add(i)
        slowerrobbers = pygame.sprite.Group()
        xslowerrobber = random.randrange(20, 430)
        yslowerrobber = random.randrange(60, 470)
        slowerrobber = SlowerRobber(xslowerrobber, yslowerrobber)
        hitwall = pygame.sprite.spritecollide(slowerrobber, walls, False)
        while len(hitwall) > 0:
            xslowerrobber = random.randrange(20, 430)
            yslowerrobber = random.randrange(60, 470)
            slowerrobber = SlowerRobber(xslowerrobber, yslowerrobber)
            hitwall = pygame.sprite.spritecollide(slowerrobber, walls, False)
        slowerrobbers.add(slowerrobber)
        allblocks.add(slowerrobber)
    return robbers, robber, allblocks, slowerrobbers, slowerrobber

    # Make accelerators and slowers
def makeaccel(stateaccel, accelers, acceler, allblocks, slowers, walls):
    if stateaccel:
        accelers = pygame.sprite.Group()
        xaccel = random.randrange(20, 430)
        yaccel = random.randrange(60, 470)
        acceler = Accelerator(xaccel, yaccel)
        hitwalls = pygame.sprite.spritecollide(acceler, walls, False)
        while len(hitwalls) > 0:
            xaccel = random.randrange(20, 430)
            yaccel = random.randrange(60, 470)
            acceler = Accelerator(xaccel, yaccel)
            hitwalls = pygame.sprite.spritecollide(acceler, walls, False)
        accelers.add(acceler)
        allblocks.add(acceler)
        slowers = pygame.sprite.Group()
    return accelers, acceler, allblocks, slowers

    # Make blocks
def makeblocks(blocks, block1, statecolor, allblocks, colorblock):
    block1 = Block(320, 320, statecolor)
    colorblock = block1.givecolor()
    blocks.add(block1)
    for i in blocks:
        allblocks.add(i)
    return blocks, block1, allblocks, colorblock

    # User moves game
def usermovesgame(done2, done3, state, player, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done2 = False
            done3 = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == 1:
                    state = 0
                else:
                    state = 1
            elif event.key == pygame.K_LEFT:
                if state == 1:
                    player.changedir(2)
            elif event.key == pygame.K_RIGHT:
                if state == 1:
                    player.changedir(1)
            elif event.key == pygame.K_UP:
                if state == 1:
                    player.changedir(3)
            elif event.key == pygame.K_DOWN:
                if state == 1:
                    player.changedir(4)
            elif event.key == pygame.K_r:
                done2 = False
                done3 = False
                play(display)
    return done2, done3, state

    # If player hits blocks
def blockshit(player, blocks, score, figure, block1, statecolor, walls, colorblock, allblocks):
    hits = pygame.sprite.spritecollide(player, blocks, True)
    if len(hits) > 0:
        score += len(hits)
        figure.changesize()
        figure.changecolor(colorblock)
        xblock = random.randrange(20, 430)
        yblock = random.randrange(60, 470)
        block1 = Block(xblock, yblock, statecolor)
        hitwall = pygame.sprite.spritecollide(block1, walls, False)
        while len(hitwall) > 0:
            xblock = random.randrange(20, 430)
            yblock = random.randrange(60, 470)
            block1 = Block(xblock, yblock, statecolor)
            hitwall = pygame.sprite.spritecollide(block1, walls, False)
        colorblock = block1.givecolor()
        blocks.add(block1)
        allblocks.add(block1)
    return blocks, score, block1, colorblock, allblocks

    # Accelerate or slow
def playeraccel(stateaccel, player, accelers, slowers):
    if stateaccel:
        hits = pygame.sprite.spritecollide(player, accelers, True)
        if len(hits) > 0:
            player.accelerate()
        hits = pygame.sprite.spritecollide(player, slowers, True)
        if len(hits) > 0:
            player.slow()
    return accelers, slowers

    # New trap
def newtrap(traps, trap2, allblocks, walls, blocks):
    traps.remove(trap2)
    allblocks.remove(trap2)
    xtrap = random.randrange(10, 440)
    ytrap = random.randrange(50, 480)
    trap2 = Trap(xtrap, ytrap)
    hitwall = pygame.sprite.spritecollide(trap2, walls, False)
    hitblock = pygame.sprite.spritecollide(trap2, blocks, False)
    while len(hitwall) > 0 or len(hitblock) > 0:
        xtrap = random.randrange(10, 440)
        ytrap = random.randrange(50, 480)
        trap2 = Trap(xtrap, ytrap)
        hitwall = pygame.sprite.spritecollide(trap2, walls, False)
        hitblock = pygame.sprite.spritecollide(trap2, blocks, False)
    traps.add(trap2)
    allblocks.add(trap2)
    return traps, trap2, allblocks

    # Remove accelerator and new slower
def newslower(stateaccel, accelers, acceler, allblocks, slowers, slower, walls):
    if stateaccel:
        if len(accelers) > 0:
            accelers.remove(acceler)
            allblocks.remove(acceler)
        slowers = pygame.sprite.Group()
        xslower = random.randrange(20, 430)
        yslower = random.randrange(60, 470)
        slower = Slower(xslower, yslower)
        hitwall = pygame.sprite.spritecollide(slower, walls, False)
        while len(hitwall) > 0:
            xslower = random.randrange(20, 430)
            yslower = random.randrange(60, 470)
            slower = Slower(xslower, yslower)
            hitwall = pygame.sprite.spritecollide(slower, walls, False)
        slowers.add(slower)
        allblocks.add(slower)
    return accelers, allblocks, slowers, slower

    # Remove slowerrobber
def removeslowerrobber(staterobber, slowerrobbers, slowerrobber, allblocks):
    if staterobber:
        if len(slowerrobbers) > 0:
            slowerrobbers.remove(slowerrobber)
            allblocks.remove(slowerrobber)
    return slowerrobber, allblocks

    # New accelerator and remove slower
def newaccel(stateaccel, accelers, acceler, walls, blocks, allblocks, slowers, slower):
    if stateaccel:
        accelers = pygame.sprite.Group()
        xaccel = random.randrange(20, 430)
        yaccel = random.randrange(60, 470)
        acceler = Accelerator(xaccel, yaccel)
        hitwall = pygame.sprite.spritecollide(acceler, walls, False)
        hitblock = pygame.sprite.spritecollide(acceler, blocks, False)
        while len(hitwall) > 0 and len(hitblock) > 0:
            xaccel = random.randrange(20, 430)
            yaccel = random.randrange(60, 470)
            acceler = Accelerator(xaccel, yaccel)
            hitwall = pygame.sprite.spritecollide(acceler, walls, False)
            hitblock = pygame.sprite.spritecollide(acceler, blocks, False)
        accelers.add(acceler)
        allblocks.add(acceler)
        if len(slowers) > 0:
            slowers.remove(slower)
            allblocks.remove(slower)
    return accelers, acceler, allblocks, slowers

    # New slowerrobber
def newslowerrobber(staterobber, slowerrobbers, slowerrobber, walls, allblocks):
    if staterobber:
        slowerrobbers = pygame.sprite.Group()
        xslowerrobber = random.randrange(20, 430)
        yslowerrobber = random.randrange(60, 470)
        slowerrobber = SlowerRobber(xslowerrobber, yslowerrobber)
        hitwall = pygame.sprite.spritecollide(slowerrobber, walls, False)
        while len(hitwall) > 0:
            xslowerrobber = random.randrange(20, 430)
            yslowerrobber = random.randrange(60, 470)
            slowerrobber = SlowerRobber(xslowerrobber, yslowerrobber)
            hitwall = pygame.sprite.spritecollide(slowerrobber, walls, False)
        slowerrobbers.add(slowerrobber)
        allblocks.add(slowerrobber)
    return slowerrobbers, slowerrobber, allblocks

    # Accelerate robbers
def robberaccel(staterobber, robbers):
    if staterobber:
        for i in robbers:
            i.accelerate()

    # Player hit traps
def playerhittraps(player, traps, done2):
    hits = pygame.sprite.spritecollide(player, traps, True)
    if len(hits) > 0:
        done2 = False
    return traps, done2

    # Player hit robber
def playerhitrobber(staterobber, player, robbers, done2):
    if staterobber:
        hits = pygame.sprite.spritecollide(player, robbers, True)
        if len(hits) > 0:
            done2 = False
    return robbers, done2

    # Robber slower
def robberslower(staterobber, player, slowerrobbers, robbers):
    if staterobber:
        hits = pygame.sprite.spritecollide(player, slowerrobbers, True)
        if len(hits):
            for i in robbers:
                i.slow()
    return slowerrobbers




# Game loop
def play(display):
    # Names
    font = pygame.font.Font("C:/Windows/Fonts/FORTE.TTF", 20)
    font2 = pygame.font.Font("C:/Windows/Fonts/STENCIL.TTF", 40)
    allblocks = pygame.sprite.Group()
    statecolor, staterobber, stateaccel = True, True, True
    xplayer, yplayer = 20, 80
    player = Player(xplayer, yplayer)
    figure = Figure(xplayer - 3, yplayer - 3, statecolor)
    traps = pygame.sprite.Group()
    trap1, trap2 = Trap(120, 120), Trap(200, 200)
    traps.add(trap1)
    traps.add(trap2)
    for i in traps:
        allblocks.add(i)
    walls = pygame.sprite.Group()
    walls, allblocks = addwalls(walls, allblocks)
    player.setwalls(walls)
    allblocks.add(player)
    clock = pygame.time.Clock()
    time = 0
    score = 0
    newhighscore = False
    done, done2, done3 = True, True, True
    state = 1
    robbers, robber, slowerrobbers, slowerrobber, slower = None, None, None, None, None
    accelers, acceler, slowers, colorblock, block1 = None, None, None, None, None
    blocks = pygame.sprite.Group()

    # Settings
    while done:
        # User moves settings
        done, done2, done3, staterobber, stateaccel, statecolor = usermovessetting(done, done2, done3, staterobber, stateaccel, statecolor, display)

        # Status
        if staterobber:
            b = 'On'
        else:
            b = 'Out'
        if stateaccel:
            c = 'On'
        else:
            c = 'Out'
        if statecolor:
            d = 'On'
        else:
            d = 'Out'

        # Display
        display.fill(black)
        write(font, 'Press space to turn robber on/off', white, display, [10, 10])
        write(font, 'Press arrow left to turn accelerator', white, display, [10, 30])
        write(font, 'on/off', white, display, [10, 50])
        write(font, 'Press arrow up to turn colorchange', white, display, [10, 70])
        write(font, 'on/off', white, display, [10, 90])
        write(font, 'Press arrow right to start', white, display, [10, 110])
        write(font, 'Robbers: ' + b, green, display, [10, 130])
        write(font, 'Accelerator: ' + c, green, display, [10, 150])
        write(font, 'Colorchange: ' + d, green, display, [10, 170])
        write(font, 'Red ghost is bad, Lightning is accelerate', blue, display, [10, 400])
        write(font, 'Snail is slow down', blue, display, [10, 420])
        write(font, 'Blue ghost is slow red ghosts', blue, display, [10, 440])
        write(font, 'Press r to restart', white, display, [10, 190])

        # Time between loops
        clock.tick(60)

        # Flip display
        pygame.display.flip()

    # Make blocks, robbers, ...
    robbers, robber, allblocks, slowerrobbers, slowerrobber = makerob(staterobber, robbers, robber, allblocks, slowerrobbers, slowerrobber, walls)
    accelers, acceler, allblocks, slowers = makeaccel(stateaccel, accelers, acceler, allblocks, slowers, walls)
    blocks, block1, allblocks, colorblock = makeblocks(blocks, block1, statecolor, allblocks, colorblock)
    figure.changestatecolor(statecolor)

    # Game
    while done2:
        # User moves game
        done2, done3, state = usermovesgame(done2, done3, state, player, display)
        
        # When game plays
        if state == 1:

            time += 1

            # Main game mechanics
            blocks, score, block1, colorblock, allblocks = blockshit(player, blocks, score, figure, block1, statecolor, walls, colorblock, allblocks)
            accelers, slowers = playeraccel(stateaccel, player, accelers, slowers)
            if (time+250)%500 == 0:
                traps, trap2, allblocks = newtrap(traps, trap2, allblocks, walls, blocks)
                accelers, allblocks, slowers, slower = newslower(stateaccel, accelers, acceler, allblocks, slowers, slower, walls)
                slowerrobber, allblocks = removeslowerrobber(staterobber, slowerrobbers, slowerrobber, allblocks)     
            if time%500 == 0:
                traps, trap1, allblocks = newtrap(traps, trap1, allblocks, walls, blocks)
                accelers, acceler, allblocks, slowers = newaccel(stateaccel, accelers, acceler, walls, blocks, allblocks, slowers, slower)
                slowerrobbers, slowerrobber, allblocks = newslowerrobber(staterobber, slowerrobbers, slowerrobber, walls, allblocks)
            if time%1500 == 0:
                robberaccel(staterobber, robbers)
            figure.changespeed(player.givecoor()[0]- 3, player.givecoor()[1]-3)
            traps, done2 = playerhittraps(player, traps, done2)
            robbers, done2 = playerhitrobber(staterobber, player, robbers, done2)
            slowerrobbers = robberslower(staterobber, player, slowerrobbers, robbers)
            if player.end > 0 or figure.end > 0:
                done2 = False
            
            # Display
            display.fill(green2)
            allblocks.update()
            allblocks.draw(display)
            figure.update()
            figure.givefigures().draw(display)
            write(font, 'Score: ' + str(score), green, display, [10, 10])

            # Time between loops
            clock.tick(60)

        # When pause
        else:
            # Display
            display.fill(black)
            write(font2, 'Pause', white, display, [100, 200])
            write(font, 'Press r to restart', white, display, [10, 10])

        # Flip display
        pygame.display.flip()

    # Highscore
    highscore = readhigh('HighscoreSnake.txt')
    newhighscore = improvehigh('HighscoreSnake.txt', newhighscore, highscore, score)
                
    # Display end
    while done3:
        # User moves game
        done2, done3, state = usermovesgame(done2, done3, state, player, display)

        # Display
        display.fill(black)
        write(font2, 'Score: ' + str(score), green, display, [0, 200])
        write(font, 'Highscore = ' + str(highscore), white, display, [70, 10])
        if newhighscore:
            write(font, 'New Highscore', green, display, [70, 30])
        write(font, 'Press r to restart', white, display, [10, 50])

        # Flip display
        pygame.display.flip()



# Main loop        
def main():
    display = init(460, 500, 'Snake')
    play(display)
    pygame.quit()


# Start game
if __name__ == '__main__':
    main()
