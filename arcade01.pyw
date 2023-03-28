import random
import pygame
from pygame.locals import *
import sys
 
pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

rawTick = 0
tick = 0

FramePerSec = pygame.time.Clock()

playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (43, 30))

pipeSectionImg = pygame.image.load('pipeSection.png')
pipeSectionImg = pygame.transform.scale(pipeSectionImg, (75, 1))

pipeTopImg = pygame.image.load('pipeTop.png')
pipeTopImg = pygame.transform.scale(pipeTopImg, (100, 50))

groundImg = pygame.image.load('ground.png')
groundImg = pygame.transform.scale(groundImg, (40,50))

scoretext = pygame.font.SysFont('Arial', 30)

gameover = False
gamestart = False
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface([43,30], pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.image = playerImg
        self.surf.blit(self.image, (0,0))
        self.rect = self.surf.get_rect()
        self.pos = vec((100, 0))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
        self.gameisrunning = True
 
    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()   
        self.vel += self.acc

        self.pos += self.vel + self.acc

        self.rect.midbottom = self.pos    

    def update(self):
        phits = pygame.sprite.spritecollide(P1, platforms, False)
        global gameover
        if phits:
            self.pos.y = phits[0].rect.top +1
            self.vel.y = 0
            gameover = True
        ohits = pygame.sprite.spritecollide(P1, pipes, False)
        if ohits:
            gameover = True

    def jump(self):
        self.vel.y = -10


 
class platform(pygame.sprite.Sprite):

    groundNum = 0

    def __init__(self):
        super().__init__()
        if platform.groundNum == 0:
            self.startpos = WIDTH
            platform.groundNum = 1
        elif platform.groundNum == 1:
            self.startpos = 0    
        self.surf = pygame.Surface([WIDTH,40], pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.image = groundImg
        for n in range(0, WIDTH // 40):
            self.surf.blit(self.image, (n*40, 0))
        self.rect = self.surf.get_rect(center = ((WIDTH/2), HEIGHT - 20))
        self.rect.x += self.startpos

    def update(self):
        self.rect.x -= 3
        if self.rect.x + WIDTH < 1:
            self.rect.x = WIDTH - 2

class pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, random.randint(50, 150)), pygame.SRCALPHA, 32)
        for n in range (0, self.surf.get_height()):
            self.surf.blit(pipeSectionImg, (12.5, n))
        self.surf.blit(pipeTopImg, (0 ,0))
        self.surf = self.surf.convert_alpha()
        self.rect = self.surf.get_rect(center = (WIDTH + 10, HEIGHT - self.surf.get_height()/2 -40))
    

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

class downPipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, random.randint(50, 150)), pygame.SRCALPHA, 32)
        for n in range (0, self.surf.get_height()):
            self.surf.blit(pipeSectionImg, (12.5, n))
        self.surf.blit(pipeTopImg, (0 ,self.surf.get_height() - 50))
        self.surf = self.surf.convert_alpha()
        self.rect = self.surf.get_rect(center = (WIDTH + 10, self.surf.get_height()/2))
    
    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

class scorezone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((1, HEIGHT), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.rect = self.surf.get_rect(center = (WIDTH + 10, HEIGHT/2))

    def update(self): 
        hits = pygame.sprite.spritecollide(P1, scorezones, False)
        self.rect.x -= 3
        if hits and gameover == False:
            P1.score += 1
            self.kill()

P1 = Player()
GROUND1 = platform()
GROUND2 = platform()

platforms = pygame.sprite.Group()
platforms.add(GROUND1)
platforms.add(GROUND2)

pipes = pygame.sprite.Group()
scorezones = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(GROUND1)
all_sprites.add(GROUND2)

rawlongTick = 0
longTick = 0
ranOnce = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if gamestart and not gameover:
                    P1.jump()
                elif not gamestart:   
                    gamestart = True
                    
                elif gamestart and gameover:
                    gameover = False
                    gamestart = False
                    P1.kill()
                    for e in pipes:
                        e.kill()
                    for e in scorezones:
                        e.kill()
                    P1 = Player()
     
    displaysurface.fill((255,255,255))
    FramePerSec.tick(FPS)
    if (gamestart and not gameover):
        rawTick += 1
        rawTick = rawTick % 20
        tick = rawTick +1
        if (tick == 10 or tick == 20):
            rawlongTick += 1
            rawlongTick = longTick % 20
            longTick = rawlongTick +1
            ranOnce = True
        if (longTick == 20 or longTick == 10) and ranOnce == True:
            pipes.add(pipe())
            pipes.add(downPipe())
            all_sprites.add(pipes)
            scorezones.add(scorezone())
            ranOnce = False
        
        pipes.update()
        platforms.update()
        scorezones.update()
    if gamestart:
        P1.move()
        P1.update()
    
    if gamestart and ranOnce:
        all_sprites.add(P1)
    if not gamestart and gameover:
        all_sprites.remove(P1)

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    
    displaysurface.blit(scoretext.render(str(P1.score), True, (0,0,0)), (WIDTH/2, 10))
    displaysurface.blit(scoretext.render(str(P1.score), True, (20,20,20)), (WIDTH/2 +2, 12))

    pygame.display.update()
    #print(tick, longTick, P1.score, P1.pos, P1.vel, P1.acc)