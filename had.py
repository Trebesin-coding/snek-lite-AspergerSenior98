# Import
import pygame
import random
# Game run 
pygame.init()
screen = pygame.display.set_mode((800, 800))
# Util
def AddDouble(d1, d2):
    x = d1[0]+d2[0]
    y = d1[1]+d2[1]
    return (x, y)

def SubtractDouble(d1, d2):
    x = d1[0]-d2[0]
    y = d1[1]-d2[1]
    return (x, y)

# Vars
running = True
clock = pygame.time.Clock()
elapsed_time = 0
fruittime = 0
nextfruit = random.randint(2000, 4000)

speed = 20
class segment: #Myslím že tohle je linked list !!! 😎 ale udělám to přes OOP at se to naucim
    def __init__(self, double, dir):
        self.dir = dir
        self.coor = (double)
        self.rect = pygame.image.load("body.png").convert_alpha()
        self.surf = self.rect.get_rect(midbottom=self.coor)
        self.NextSegment = None
    def Grow(self):
        if self.NextSegment == None:
            newCoor = SubtractDouble(self.coor, self.dir)
            self.NextSegment = segment(newCoor, SubtractDouble(self.coor, newCoor))
        else:
            self.NextSegment.Grow()
    def Blit(self):
        self.surf = self.rect.get_rect(midbottom=self.coor)
        screen.blit(self.rect, self.surf)
    def Move(self):
        self.coor = AddDouble(self.coor, self.dir)
        self.Blit()
        #print(self.NextSegment)
        if self.NextSegment != None:
            self.NextSegment.Move()
            self.NextSegment.UpdateDir(self.dir)
            
    def UpdateDir(self, newDir):
        if newDir == self.dir:
            return
        if self.NextSegment != None: #předat direction dalšímu segmentu
            self.NextSegment.UpdateDir(self.dir)
        self.dir = newDir
    def CrashCheck(self, comparedCoor):
        if self.coor == comparedCoor:
            return True
        elif self.NextSegment != None and self.NextSegment.CrashCheck(comparedCoor) == True:
            return True
        else:
            return False
    
class Head(segment):
    def __init__(self, double, dir):
        super().__init__(double, dir)
        self.rect = pygame.image.load("head.png").convert_alpha()
        self.moving = True
    def canIMove(self):
        targetCoor = AddDouble(self.coor, self.dir)
        if self.NextSegment != None and self.NextSegment.CrashCheck(targetCoor) == True:
            self.Crash()
        else:
            if fruit != None and targetCoor == fruit.coor: # Vim ze muzu pouzit kolizi ale nepouziju
                self.Grow()
                fruit.active = False
            self.Move()
    def Crash(self):
        self.moving = False
        self.rect = pygame.image.load("dead.png").convert_alpha()
        self.Blit()

class Fruit:
    def __init__(self, active):
        coor = head.coor
        while True:
            coor = (random.randrange(39)*20,random.randrange(39)*20)
            if head.CrashCheck(coor) == False: # At se nespawnuje na okupované místo
                break
        self.coor = coor
        self.active = active
        self.rect = pygame.image.load("fruit.png").convert_alpha()
        self.surf = self.rect.get_rect(midbottom=self.coor)
    def Blit(self):
        self.surf = self.rect.get_rect(midbottom=self.coor)
        screen.blit(self.rect, self.surf)

head = Head((400, 400), (0,0))
fruit = Fruit(False)


# Render loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
    #Input
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        
        head.UpdateDir((0, -speed))
    if key[pygame.K_a]:
        head.UpdateDir((-speed, 0))
    if key[pygame.K_s]:
        head.UpdateDir((0, speed))
    if key[pygame.K_d]:
        head.UpdateDir((speed, 0))

    #Render
    
    
    if elapsed_time > 120 and head.moving == True: # at fps nelimituje inputy
        screen.fill("Black")
        ##Player
        head.canIMove()
        elapsed_time = 0
    ##Fruit
        if fruit.active == False:
            if fruittime > nextfruit:
                fruit = Fruit(True)
                fruittime = 0
                nextfruit = random.randint(1200, 3200)
        elif head.moving == True:
            fruit.Blit()
    pygame.display.update()
    #Clock
    elapsed_time += clock.get_time()
    fruittime += clock.get_time()
    clock.tick(60)
