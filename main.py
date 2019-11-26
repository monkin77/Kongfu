import pygame
import math, random, sys

def events():
    for event in pygame.event.get():
        if event.type == "QUIT" or (event.type == "KEYDOWN" and event.key == "K_ESCAPE"):
            pygame.quit()
            sys.exit()

#defien display surface
W,H = 1920, 1080
HW,HH = W/2, H/2
AREA = W*H

#INITIALIZE DISPLAY
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("Kong Fu")
FPS = 1

#Define colors
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
GREEN = (0,255,0,0)



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

index = 0
while True:
    events()
    DS.fill(GREEN)
    s = spritesheet("zelda_standing.png", 1,1)
    s.draw(DS, index%s.totalCellCount, HW,HH, 4)  #Center handle = 4
    index += 1
    pygame.display.update()
    CLOCK.tick(FPS)