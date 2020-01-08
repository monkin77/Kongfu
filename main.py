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

score = 0
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
        self.handle = list ([ (0,0),(-hw,0),(-w,0), (0,-hh), (-hw,-hh), (-w,-hh), (0,-h), (-hw,-h), (-w,-h),])

    def draw(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet, (x+self.handle[handle][0], y+ self.handle[handle][1]), self.cells[cellIndex])
        
#walkRight = spritesheet("C:/Users/joaog/OneDrive/Desktop/FEUP/1 ano/fpro/Kongfu/zelda_Rwalk2b.png",6,1)
walkRight = spritesheet("sprites/zelda_Rwalk2b.png",6,1)
walkLeft = spritesheet("sprites/zelda_Lwalk2b.png",6,1)     #100 X 120 px
standing = spritesheet("sprites/zelda_standing2.png",1,1)
background = pygame.image.load("sprites/wallpaper.gif")
l_punch = spritesheet("sprites/zelda_Lpunchb.png",1,1)
r_punch = spritesheet("sprites/zelda_Rpunchb.png",1,1)
l_bow = spritesheet("sprites/zelda_Lbowb.png",4,1)
r_bow = spritesheet("sprites/zelda_Rbowb.png",4,1)       #corrigir as imagens
l_arrow = spritesheet("sprites/l_arrow.png",1,1)
r_arrow = spritesheet("sprites/r_arrow.png",1,1)
r_ghost = spritesheet("sprites/r_ghostb.gif",1,1)
l_ghost = spritesheet("sprites/l_ghostb.png",1,1)
r_koopa = spritesheet("sprites/koopas_rightb.gif",3,1)
l_koopa = spritesheet("sprites/koopas_leftb.gif",3,1)
l_dragon = pygame.image.load("sprites/l_dragonb.png")
r_dragon = pygame.image.load("sprites/r_dragonb.png")
bow_sound = pygame.mixer.Sound("sound/bow_sound.wav")
bow_hit_sound = pygame.mixer.Sound("sound/bow_hit_sound.wav")
punch_sound = pygame.mixer.Sound("sound/punch.wav")
game_over = pygame.mixer.Sound("sound/game_over.wav")



class enemy(object):
    def __init__(self,x,y,width,height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        if self.path[1] > self.path[0]:
            self.vel = 3
        else:
            self.vel = -3
        self.health = 10
        self.visible = True
        self.hitbox = (self.x+17,self.y +2, self.width,self.height)
        self.hp_bar = (self.x-self.width/2+20,self.y-self.height/2-15,50, 12)
    
    def draw(self,win):
        self.move()
        if self.walkCount >= 30:
            self.walkCount = 0
        if self.visible:
            if self.vel > 0:
                r_koopa.draw(win,self.walkCount // 10,self.x, self.y,4)
                self.walkCount += 1
            else:
                l_koopa.draw(win,self.walkCount // 10, self.x, self.y,4)
                self.walkCount += 1

        self.hitbox = (self.x-self.width/2+10,self.y-self.height/2,self.width-22,self.height)
        self.hp_bar = (self.x-self.width/2+20,self.y-self.height/2-15,50, 12)
        #pygame.draw.rect(win,(255,0,0),self.hitbox)    hitbox
        pygame.draw.rect(win, (255,0,0), self.hp_bar)   #red hp
        pygame.draw.rect(win, (0,255,0), (self.hp_bar[0], self.hp_bar[1], 5*self.health, self.hp_bar[3]))   #green hp

    def move(self):
        #if man.hitbox[0] <= self.hitbox[0] <= man.hitbox[0] + man.hitbox[2]:
        #    self.vel = self.vel * -1
        if self.vel > 0:
            if self.x + self.vel < max(self.path[1], self.path[0]):
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
        else:
            if self.x + self.vel > min(self.path[0], self.path[1]):
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel

    def arrow_hit(self):
        print("arrow hit")
        bow_hit_sound.play()
        global score
        if self.health > 0:
            self.health -= 10
            if man.left:
                self.x -= 20
            else:
                self.x += 20
        if self.health <= 0:
            score += 1
            self.visible = False
    def punch_hit(self):
        global score
        print("FALCON PUUUUNCH")
        if self.health > 0:
            self.health -= 5
            self.vel *= -1
        if self.health <= 0:
            score += 1
            self.visible = False




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
        self.punchCount = 0
        self.bow = False
        self.bowCount = 0
        self.arrow = False
        self.walkCount = 0
        self.immortal = False
        self.immortalCount = 0
        self.visible = True
        self.health = 10
        self.hitbox = (self.x-self.width/2,self.y-self.height/2,self.width,self.height)
        self.hp_bar = (self.x-self.width/2+20,self.y-self.height/2-15,self.width-40, 15)
        #self.punchCount = 0     #new
        #self.kickCount = 0
        self.isJump = False
        self.jumpCount = 10
    def draw(self,win):
        self.hitbox = (self.x-self.width/2,self.y-self.height/2,self.width,self.height)
        self.hp_bar = (self.x-self.width/2+20,self.y-self.height/2-15,50, 12)
        if self.walkCount +1 >= 30:
            self.walkCount = 0
        if self.bowCount +1 >= 60:
            self.arrow = True
            self.bowCount = 0
        #if self.punchCount +1 >= 30:
         #   self.punchCount = 0
        
        if self.immortalCount == 90:
            self.immortal = False

        if not (self.punch) and not(self.bow):      #changes
            if not(self.standing):
                if self.left:
                    #win.blit(walkLeft[self.walkCount // 5], (self.x,self.y))
                    walkLeft.draw(win, self.walkCount//5, self.x,self.y, 4)  #Center handle = 4
                    self.walkCount += 1
                    self.immortalCount += 1
                elif self.right:
                    #win.blit(walkRight[self.walkCount //5], (self.x,self.y))
                    walkRight.draw(win, self.walkCount//5, self.x,self.y, 4)
                    self.walkCount += 1
                    self.immortalCount += 1
            else:
                if self.right:
                    #win.blit(walkRight[0],(self.x,self.y))
                    walkRight.draw(win, 0, self.x,self.y, 4)
                    self.immortalCount += 1
                elif self.left:
                    #win.blit(walkLeft[5], (self.x,self.y))
                    walkLeft.draw(win, 5, self.x,self.y, 4)
                    self.immortalCount += 1
                else:
                    #win.blit(standing, (self.x,self.y))
                    standing.draw(win, 0, self.x,self.y, 4)
                    self.immortalCount += 1

        elif self.punch:
            self.immortalCount += 1
            punch_sound.play()
            if self.left:
                l_punch.draw(win,0,self.x,self.y,4)
                #self.punch += 1
            elif self.right:
                r_punch.draw(win,0,self.x,self.y,4)
                #self.punch += 1
        
        elif self.bow:
            self.immortalCount += 1
            if self.bowCount // 15 == 1:
                bow_sound.play()
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
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)          hitbox
        pygame.draw.rect( win,(255,0,0), self.hp_bar)         #hp rect
        pygame.draw.rect( win,(0,255,0), (self.hp_bar[0], self.hp_bar[1], 5 * self.health, self.hp_bar[3]))             # green rect hp

    def hit(self):
        print("Player hit")
        if self.health > 0 and self.immortal == False:
            self.health -= 1
            self.immortal = True
            self.immortalCount = 0
            #self.x = 20
        else:
            self.visible = False
class projectiles(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 10 *facing
        self.width = 80
        self.height = 30
    def draw(self,win):
        if self.facing == 1:
            r_arrow.draw(win,0,self.x,self.y,4)
        elif self.facing == -1:
            l_arrow.draw(win,0,self.x,self.y,4)
        self.hitbox = (self.x-self.width/2,self.y+10-self.height/2,self.width,self.height)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


def redrawGameWindow():
    global walkCount
    global run
    if run:
        win.blit(background,(0,170))
        pygame.draw.rect(win,(80,30,0), (0,0,W,170))
        pygame.draw.rect(win,(80,30,0), (0,720-147,W,170))
        win.blit(l_dragon,(-10,0))
        win.blit(r_dragon,(W-110,0))
        title = font3.render("Kong Fu", 1, (255,255,255))
        score_count = font2.render("Score: " + str(score), 1, (255,255,255))
        win.blit(title,(W/2-100,50))
        win.blit(score_count, (W-200,120))
        man.draw(win)
        for arrow in arrows:
            arrow.draw(win)
        for enemy in enemies:
            enemy.draw(win)
    #ghost.draw(win,0,300,400,4)
    else:
        pygame.time.delay(100)
        win.fill(BLACK)
        text = font4.render("Game over", 1, (255,0,0))
        win.blit(text, (W/2-340,H/2-150))
        game_over.play()
        pygame.display.update()
        pygame.time.delay(1000)
    pygame.display.update()

#main loop
man = player(300,500,110,150)   #Check width and height
font1 = pygame.font.SysFont('comicsans', 70, False, True) #(font, size, bold, italicized)
font2 = pygame.font.SysFont('comicsans', 40, False, False) #(font, size, bold, italicized)
font3 = pygame.font.SysFont('javanesetext', 55, False, False)
font4 = pygame.font.SysFont('vivaldi',180, False, False)
arrows = []
#koopa = enemy(100,500,90,90,450)
enemies = []
run = True
counter = 0
hit_count = 0


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


    if len(enemies) < (score // 5)+2:           # increases the amount of koopas when the score reaches a multiple of 5
        pos_x = random.randint(40,930)
        while abs(pos_x-man.x) <= 60:
             pos_x = random.randint(40,930)
        if counter > 150:
            counter = 0
        counter += 1
        #print(pos_x)
        if pos_x < 480 and counter == 1:
            end = pos_x + 400
            enemies.append(enemy(pos_x,500,90,90,end))
        elif pos_x >= 480 and counter == 1:
            end = pos_x - 400
            enemies.append(enemy(pos_x,500,90,90,end))
    
    for koopa in enemies:
        if koopa.visible:
            for arrow in arrows:
                if arrow.hitbox[0] > koopa.hitbox[0] and arrow.hitbox[0] < koopa.hitbox[0] + koopa.hitbox[2]:
                    koopa.arrow_hit()
                    if koopa.health <= 0:
                        del enemies[enemies.index(koopa)]
                    arrows.pop(arrows.index(arrow)) #remove the arrow
    
    for koopa in enemies:
        if koopa.visible:
            if man.punch and man.punchCount == 1:
                #hit_count = 0
                if ( koopa.hitbox[0] < man.hitbox[0] < koopa.hitbox[0] + koopa.hitbox[2]) or ( man.hitbox[0] < koopa.hitbox[0] < man.hitbox[0] + man.hitbox[2]):
                    koopa.punch_hit()
                    if koopa.health <= 0:
                        del enemies[enemies.index(koopa)]
            else:
                if ( koopa.hitbox[0] < man.hitbox[0]+man.width/2  < koopa.hitbox[0] + koopa.hitbox[2]) or ( man.hitbox[0] < koopa.hitbox[0]+koopa.width/2  < man.hitbox[0] + man.hitbox[2]):    #slight adjustments
                    man.hit()   
                    koopa.vel = koopa.vel * -1      

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and man.x >=man.vel: #It has to be greater or equal to vel so it doesnt go out of the map
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        man.punch = False
        man.punchCount = 0
        man.bow = False
    elif keys[pygame.K_RIGHT] and man.x < W - man.vel - man.width/2: 
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
        man.punch = False
        man.punchCount = 0
        man.bow = False
    elif keys[pygame.K_a]:
        man.punchCount += 1
        man.punch = True
        man.bow = False
        man.standing = False
    elif keys[pygame.K_s]:
        man.bow = True
        man.punch = False
        man.punchCount = 0
        man.standing = False
    else:
        man.standing = True
        man.bow = False
        man.punch = False
        man.punchCount = 0
        man.walkCount = 0
        #man.punchCount = 0
        #man.kickCount = 0

    if keys[pygame.K_g]:        #Hotkey to gameOver
        run = False

    if man.health <= 0:
        run = False

    redrawGameWindow()
    

