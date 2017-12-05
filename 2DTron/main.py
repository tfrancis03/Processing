#This is our game sdafds
print('hello world')

#Expand for the complete game class.
import pygame
import random
import math
import sys
from pygame.locals import *
from Player import *
from Direction import *
from enum import Enum

class Screen(Enum):
    Menu = 1
    Play = 2 
    EndGame = 3
    Stats = 4

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
death = pygame.mixer.Sound('Sounds/death.wav')


#PlayMusic = pygame.mixer.music.play('Sounds/play.mp3')


currentScreen = Screen.Menu
pygame.init()
# Screen 
screen = pygame.display.set_mode((800, 750))
background =  pygame.Surface((800, 750), 0, screen)
pygame.display.set_caption('If u see this ur too close!')
backColor = Color('black')
background.fill(backColor)
screen.blit(background, (0, 0))
font = pygame.font.SysFont(None, 36)
# Player 
player1 = Player(250,250,'red')
player2 = Player(450,450,'blue')
playerGroup = pygame.sprite.Group()
playerGroup.add(player1)
playerGroup.add(player2)
gameOver = False
p1Winner = False
initialized = False
addTimer = 0.0 # keeps track of when to add new trails to a player
removeTimer = 0.0
pathTime = 19
removeDelay = 1000
removePathTime = removeDelay + 80
turnTimer = 0.0     
mainClock = pygame.time.Clock()
p1wins = 0
p2wins = 0
menuInit = False
playInit = False
AIUse = False
doubleAI = False
testMode = False
boringTimer = 200
boringTimer2 = 200
sameDirTimer = 0
sameDirInterval = 2000
changeTimer = 20000


def menu(screen):
    global currentScreen, menuInit, AIUse

    
    if not menuInit:
        menuMusic = pygame.mixer.music.load('Sounds/Menu.wav')
        pygame.mixer.music.play()
        
        menuInit = True
        
    
    
    pos = (-1,-1)
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
    
    screen.fill(pygame.Color(109,0,233))
    keys = pygame.key.get_pressed()
    if keys[K_t]:
        AIUse = True
        test()
        currentScreen = Screen.Play
        testMode = True
    
    statsButton = pygame.Rect(150,375,200,100)
    statsButtonImage = pygame.Surface([200, 100])
    statsButtonImage.fill(pygame.Color('orange'))
    screen.blit(statsButtonImage, statsButton)    
    
    if statsButton.collidepoint(pos[0], pos[1]):
        currentScreen = Screen.Stats
      
    AIButton = pygame.Rect(450,500,200,100)
    AIImage = pygame.Surface([200, 100])
    if not AIUse:
        AIImage.fill(pygame.Color('green'))
    else:
        AIImage.fill(pygame.Color('brown'))
    screen.blit(AIImage, AIButton)    
    
    playAgainButton = pygame.Rect(450,375,200,100)
    playAgainImage = pygame.Surface([200, 100])
    playAgainImage.fill(pygame.Color('blue'))
    screen.blit(playAgainImage, playAgainButton)    

    if playAgainButton.collidepoint(pos[0], pos[1]):
        initPlayers()
        currentScreen = Screen.Play
        pos = (-1,-1)

    if AIButton.collidepoint(pos[0], pos[1]):
        AIUse = not AIUse
        
        pos = (-1,-1)

            
        
    draw_text('BOXOTRON',screen,85,100,150) 
    
    if not AIUse:
        draw_text('Turn on AI',screen,490,535)
    else:
        draw_text('Turn off AI',screen,485,535)
    draw_text('Play',screen,525,410) 
    draw_text('Stats',screen,215,410) 


def stats(screen):
    global p1wins, p2wins,currentScreen
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
            currentScreen = Screen.Menu
    
    screen.fill(pygame.Color('orange'))
    draw_text('P1 Wins: ' + str(p1wins), screen, 150, 200, 100)
    draw_text('P2 Wins: ' + str(p2wins), screen, 150, 500, 100)

def endGame(screen):
    global currentScreen
    
    pos = (-1,-1)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        
    pos = pygame.mouse.get_pos()
    initPlayers()

    
    screen.fill(pygame.Color('dark red'))
    playAgainButton = pygame.Rect(450,375,200,100)
    playAgainImage = pygame.Surface([200, 100])
    playAgainImage.fill(pygame.Color('blue'))
    screen.blit(playAgainImage, playAgainButton)    

    menuButton = pygame.Rect(150,375,200,100)
    menuImage = pygame.Surface([200, 100])
    menuImage.fill(pygame.Color('blue'))
    screen.blit(menuImage, menuButton)  
    draw_text('Menu',screen,210,410)  
    draw_text('Play Again',screen,490,410) 
    if p1Winner:
        draw_text('Player 2 Wins', screen, 175, 100,100)
    else:
        draw_text('Player 1 Wins', screen, 175, 100,100)
    

    #400,375,200,100

    if menuButton.collidepoint(pos[0], pos[1]):
        currentScreen = Screen.Menu
        pos = (-1,-1)
    elif playAgainButton.collidepoint(pos[0], pos[1]):
        currentScreen = Screen.Play
        pos = (-1,-1)

    
    

def draw_text(display_string, surface, x_pos, y_pos, size=36):
    font = pygame.font.SysFont(None, size)
    text_display = font.render(display_string, 1, Color('White'))
    surface.blit(text_display, (x_pos, y_pos))
    
def initPlayers():
    global removeTimer, mainClock,addTimer, removeDelay,removePathTime, player1, player2, playerGroup # Reset/Initialize Players, Get rid of Trails?
    player2.turnHistory = list()
    player1 = Player(250,250,'red')
    player2 = Player(450,450,'blue')
    playerGroup = pygame.sprite.Group()
    playerGroup.add(player1)
    playerGroup.add(player2)
    removeDelay = 15000
    removePathTime = removeDelay + 80
    removeTimer = 0.0
    addTimer = 0.0
    player2.addTurn()
    mainClock = pygame.time.Clock()
    
def test():
    global player1, player2, screen
    initPlayers()
    player1.dir = Direction.STILL
    player1.x = 600
    player1.y = 600
    player1.testTrails()
    player2.dir = Direction.DOWN
    player2.x = 350
    player2.y = 350

def play(screen):
    global changeTimer, boringTimer2, boringTimer, AIUse,playInit, p1wins, p2wins, player1, player2, gameOver, p1Winner, font, initialized, addTimer, removeTimer, pathTime, removeDelay, removePathTime, turnTimer, mainClock, currentScreen
    global sameDirTimer, sameDirInterval
    
    if not playInit:
        menuMusic = pygame.mixer.music.load('Sounds/Play.wav')
        pygame.mixer.music.play()
        
        playInit = True
        
    if not initialized:
        
        screen.fill(pygame.Color('black'))
        player1.clear(250,250)
        player2.clear(450,450)
        initPlayers()
        
        
        initialized = True
    gameOver = False
    p1Winner = False
    
    # Timers
    
        
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Set direction for Player 1
    keys = pygame.key.get_pressed()
    
    if not doubleAI:
        if keys[K_a] and player1.turnTimer <= 0:
            player1.setDir(Direction.LEFT)
            player1.turnTimer = 400.0
        if keys[K_d] and player1.turnTimer <= 0:
            player1.setDir(Direction.RIGHT)
            player1.turnTimer = 400.0
        if keys[K_w] and player1.turnTimer <= 0:
            player1.setDir(Direction.UP)
            player1.turnTimer = 400.0
        if keys[K_s] and player1.turnTimer <= 0:
            player1.setDir(Direction.DOWN)
            player1.turnTimer = 400.0
    
    else:
        #computer to make decision on its own
        dir = player1.AITurn(player2,screen)
        if player1.turnTimer <= 0 and dir != player1.dir:
            player1.setDir(dir)
            player1.turnTimer = 0.0
#         elif player1.turnTimer <= 0 and boringTimer2 <= 0:
#             if player1.edgeTurn(0.1) != dir:
#                 player1.setDir(player1.edgeTurn(0.1))
#             
#                 player1.turnTimer = 0.0
#                 boringTimer2 = random.randint(10,20)*100
    
    if not AIUse:
        if keys[K_LEFT] and player2.turnTimer <= 0:
            player2.setDir(Direction.LEFT)
            player2.turnTimer = 400.0
        if keys[K_RIGHT] and player2.turnTimer <= 0:
            player2.setDir(Direction.RIGHT)
            player2.turnTimer = 400.0
        if keys[K_UP] and player2.turnTimer <= 0:
            player2.setDir(Direction.UP)
            player2.turnTimer = 400.0
        if keys[K_DOWN] and player2.turnTimer <= 0:
            player2.setDir(Direction.DOWN)
            player2.turnTimer = 400.0 
    else:
        #computer to make decision on its own
        dir = player2.AITurn(player1,screen)
        if player2.turnTimer <= 0 and dir != player2.dir and dir != player2.boxTurn:
            player2.setDir(dir) # setting dir here, even though dir could box itself in
            player2.turnTimer = 0.0
            player2.addTurn() # try to correct dir, if we box ourselves in
            player2.removeTurn()
            sameDirTimer = 0 #change in direction -> reset timer
        elif player2.turnTimer <= 0 and boringTimer <= 0 and player2.boxTurn == None:
            if player2.edgeTurn(0.1) != dir:
                player2.setDir(player2.edgeTurn(0.1))
                
                player2.turnTimer = 0.0
                boringTimer = random.randint(10,20)*100         #FIX BOXTURN. MAKE AITURN AND THE EDGETURN SYSTEM HAVE TO GO THROUGH THE BOXTURN BEFORE BOXING ITSELF IN.
                player2.addTurn()
                sameDirTimer = 0
                player2.removeTurn()
                
        # Let the AI box itself in after a certain amount of time going in the same direction
        if player2.dir == dir:
            sameDirTimer += mainClock.get_time()
        if(sameDirTimer > sameDirInterval):
            player2.forceRemoveTurn()
            sameDirTimer = 0
        
                
        print(player2.turnList)
        print(player2.turnHistory)
        print(player2.boxTurn)

      
    if keys[K_t]:
        AIUse = True
        test()
        currentScreen = Screen.Play
        
    if keys[K_p]:
        player1.x = player2.x/2
        player2.x = player2.x/2
        player1.y = player2.y/2
        player2.y = player2.y/2
    changeTimer -= mainClock.get_time()
    addTimer += mainClock.get_time()
    removeTimer += mainClock.get_time()
    turnTimer -= mainClock.get_time()
    if not player2.edgeCheck(0.1):
        boringTimer = random.randint(10,20)*100
        
    boringTimer -= mainClock.get_time()
    if not player1.edgeCheck(0.1):
        boringTimer2 = random.randint(10,20)*100
        
    boringTimer2 -= mainClock.get_time()

    mainClock.tick(30)
        
    if addTimer > pathTime:
        #create new paths here  
        if not testMode:
            player1.addBlock()
            player2.addBlock()
        addTimer = 0
        
    if removeTimer > removePathTime:
        # call removeBlock
        player1.removeBlock()
        player2.removeBlock()

        removeTimer = removeDelay
    
    if player1.collideBorders(800,750):
        player1.setDir(Direction.STILL)
        #freeze for now, die later.
        
    if player2.collideBorders(800,750):
        player2.setDir(Direction.STILL)
        #freeze for now, die later.
    if player1.collideWithOther(player2):
        death.play()
        #player1 dies
        #player 1 is STILL
        #Display Player 1 Won
        gameOver = True
        p2wins+=1
        p1Winner = True
    
    if player2.collideWithOther(player1):
        death.play()
        #player2 dies
        gameOver = True
        p1wins+=1
        p1Winner = False
    
    if player1.collideWithSelf():
        death.play()
        gameOver = True
        p2wins+=1
        p1Winner = True
    
    player2.update(mainClock.get_time())
    player1.update(mainClock.get_time())

    if player2.collideWithSelf():
        death.play()
        gameOver = True
        p1wins+=1
        p1Winner = False
    screen.fill(backColor)
    playerGroup.clear(screen, background)
    playerGroup.draw(screen)
    player1.drawTrail(screen)
    player2.drawTrail(screen)
    
    #player2.drawHitBoxes(screen)
    #player1.drawHitBoxes(screen)

    if(gameOver):    
        currentScreen = Screen.EndGame
    
while True:
    if currentScreen == Screen.Menu:
        menu(screen)
    if currentScreen == Screen.Play:
        play(screen)
    if currentScreen == Screen.EndGame:
        endGame(screen)
    if currentScreen == Screen.Stats:
        stats(screen)
    
        
    if currentScreen != Screen.Menu:
        menuInit = False
    if currentScreen != Screen.Play:
        playInit = False
    pygame.display.update()
    
        
    
    
    