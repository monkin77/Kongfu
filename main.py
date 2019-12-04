import pygame
import math, random, sys

#define display surface
W,H = 960,720
HW,HH = W/2, H/2
AREA = W*H

#INITIALIZE DISPLAY
pygame.init()
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("Kong Fu")
FPS = 60

#Define colors
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
GREEN = (0,255,0,0)

#LOADING SPRITES

class spritesheet:
    def __init__(self, filename,cols,rows):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols*rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / cols
        h = self.cellHeight = self.rect.height / rows
        hw,hh = self.cellCenter = (w/2, h/2)

        self.cells = list([(index%cols * w,index//cols*h,w,h) for index in range(self.totalCellCount)])
        self.handle = list ([ (0,0),(-hw,0), (-w,0), (0,-hh), (-hw,-hh), (-w,-hh), (0,-h), (-hw,-h), (-w,-h),])

    def draw(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet, (x+self.handle[handle][0], y+ self.handle[handle][1]), self.cells[cellIndex])

walkRight = spritesheet("zelda_Rwalk2b.png",6,1)
walkLeft = spritesheet("zelda_Lwalk2b.png",6,1)     #100 X 120 px
standing = spritesheet("zelda_standing2.png",1,1)
background = pygame.image.load("wallpaper.gif")
l_punch = spritesheet("zelda_Lpunchb.png",1,1)
r_punch = spritesheet("zelda_Rpunchb.png",1,1)
l_bow = spritesheet("zelda_Lbowb.png",4,1)
r_bow = spritesheet("zelda_Rbowb.png",4,1)       #corrigir as imagens
l_arrow = spritesheet("l_arrow.png",1,1)
r_arrow = spritesheet("r_arrow.png",1,1)
#l_bow = [pygame.image.load("zelda_Lbowb4.png"),pygame.image.load("zelda_Lbowb3.png"),pygame.image.load("zelda_Lbowb2.png"),pygame.image.load("zelda_Lbowb1.png")]


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.standing = True
        self.punch = False  #new
        self.bow = False
        self.bowCount = 0
        self.arrow = False
        self.walkCount = 0
        #self.punchCount = 0     #new
        #self.kickCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.hitbox = (self.x+17,self.y+11,40,40)
    def draw(self,win):
        if self.walkCount +1 >= 30:
            self.walkCount = 0
        if self.bowCount +1 >= 60:
            self.arrow = True
            self.bowCount = 0
        #if self.punchCount +1 >= 30:
         #   self.punchCount = 0
        
        if not (self.punch) and not(self.bow):      #changes
            if not(self.standing):
                if self.left:
                    #win.blit(walkLeft[self.walkCount // 5], (self.x,self.y))
                    walkLeft.draw(win, self.walkCount//5, self.x,self.y, 4)  #Center handle = 4
                    self.walkCount += 1
                elif self.right:
                    #win.blit(walkRight[self.walkCount //5], (self.x,self.y))
                    walkRight.draw(win, self.walkCount//5, self.x,self.y, 4)
                    self.walkCount += 1
            else:
                if self.right:
                    #win.blit(walkRight[0],(self.x,self.y))
                    walkRight.draw(win, 0, self.x,self.y, 4)
                elif self.left:
                    #win.blit(walkLeft[5], (self.x,self.y))
                    walkLeft.draw(win, 5, self.x,self.y, 4)
                else:
                    #win.blit(standing, (self.x,self.y))
                    standing.draw(win, 0, self.x,self.y, 4)

        elif self.punch:
            if self.left:
                l_punch.draw(win,0,self.x,self.y,4)
                #self.punch += 1
            elif self.right:
                r_punch.draw(win,0,self.x,self.y,4)
                #self.punch += 1
        
        elif self.bow:
            if self.left:
                if self.arrow == True:
                    arrows.append(projectiles(self.x-70,self.y-15,-1))
                    self.arrow = False

                l_bow.draw(win,int(self.bowCount//15),self.x,self.y,4)
                #win.blit(l_bow[int(self.bowCount//15)],(self.x-62.5,self.y-60))
                self.bowCount += 1
            elif self.right:
                if self.arrow == True:
                    arrows.append(projectiles(self.x+70,self.y-15,1))
                    self.arrow = False
                r_bow.draw(win,int(-self.bowCount//15),self.x,self.y,4)
                self.bowCount += 1

class projectiles(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 10 *facing
    def draw(self,win):
        if self.facing == 1:
            r_arrow.draw(win,0,self.x,self.y,4)
        elif self.facing == -1:
            l_arrow.draw(win,0,self.x,self.y,4)


def redrawGameWindow():
    global walkCount
    win.blit(background,(0,170))
    pygame.draw.rect(win,(80,30,0), (0,0,W,170))
    pygame.draw.rect(win,(80,30,0), (0,720-147,W,170))
    man.draw(win)
    for arrow in arrows:
        arrow.draw(win)
    pygame.display.update()

    

#main loop
man = player(300,500,100,150)
arrows = []


run = True

while run:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for arrow in arrows:
        #gotta add stuff enemy colisions

        if arrow.x < W and arrow.x > 0:
            arrow.x += arrow.vel
        else:
            arrows.pop(arrows.index(arrow)) #remove the arrow if it goes outside bounds
    





    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and man.x >=man.vel: #It has to be greater or equal to vel so it doesnt go out of the map
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        man.punch = False
        man.bow = False
    elif keys[pygame.K_RIGHT] and man.x < W - man.width - man.vel: 
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
        man.punch = False
        man.bow = False
    elif keys[pygame.K_a]:
        man.punch = True
        man.bow = False
        man.standing = False
    elif keys[pygame.K_s]:
        man.bow = True
        man.punch = False
        man.standing = False
        
    else:
        man.standing = True
        man.bow = False
        man.punch = False
        man.walkCount = 0
        #man.punchCount = 0
        #man.kickCount = 0

    redrawGameWindow()