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
FPS = 30

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

walkRight = spritesheet("C:/Users/joaog/OneDrive/Desktop/FEUP/1 ano/fpro/Kongfu/zelda_Rwalk2b.png",6,1)
walkLeft = spritesheet("C:/Users/joaog/OneDrive/Desktop/FEUP/1 ano/fpro/Kongfu/zelda_Lwalk2b.png",6,1)
standing = spritesheet("C:/Users/joaog/OneDrive/Desktop/FEUP/1 ano/fpro/Kongfu/zelda_standing2.png",1,1)
background = pygame.image.load("C:/Users/joaog/OneDrive/Desktop/FEUP/1 ano/fpro/Kongfu/wallpaper.gif")



index = 0

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
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.hitbox = (self.x+17,self.y+11,40,40)
    def draw(self,win):
        if self.walkCount +1 >= 30:
            self.walkCount = 0
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



def redrawGameWindow():
    global walkCount
    win.blit(background,(0,170))
    pygame.draw.rect(win,(80,30,0), (0,0,W,170))
    pygame.draw.rect(win,(80,30,0), (0,720-147,W,170))
    man.draw(win)
    pygame.display.update()

#main loop
man = player(300,500,100,150)



run = True

while run:
    CLOCK.tick(FPS)
    redrawGameWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and man.x >=man.vel: #It has to be greater or equal to vel so it doesnt go out of the map
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < W - man.width - man.vel: 
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0



    #redrawGameWindow()
    #s = spritesheet("zelda_Lwalk2.png", 6,1)
    #s.draw(win, index%s.totalCellCount, HW,400, 4)  #Center handle = 4
    #index += 1
    pygame.display.update()
    redrawGameWindow()