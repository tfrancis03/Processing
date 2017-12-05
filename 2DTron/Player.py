

#Expand to see the player class.
import random
import pygame
from Direction import *
from Trail import Trail

class Player(pygame.sprite.Sprite):

    image = None
    speed = 5
    turnTimer = 0.0
    turnHistory = list() #keep track of the past 3 moves, FIFO
    boxTurn = None # the move that will result into Player boxing itself in
    turnList = list()
    #When a coin is created, provide an x and
    #y position for it to be drawn at.
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.width = 20
        self.dir = self.randomDir()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.image = pygame.Surface([self.width, self.width])
        self.image.fill(pygame.Color(color))
        self.trail = Trail(5, 5, color)
        self.hitBoxes = dict()
        self.updateHitBoxes()
        ##print(isinstance(self.rect, pygame.Rect))
    
    def addTurn(self):
        self.turnHistory.append(self.dir)
        self.turnList = self.interpretTurns() 
        #which turn is restricted? Which turn will box ourself
        self.boxTurn = self.getBoxTurn()
        
    def removeTurn(self):
        while(len(self.turnHistory) > 3):
            self.turnHistory.pop(0)
            self.boxTurn = self.getBoxTurn()
            
    def forceRemoveTurn(self):
        if(len(self.turnHistory) > 0):
            self.turnHistory.pop(0)
            self.boxTurn = self.getBoxTurn()

            
    def getBoxTurn(self):
        if(len(self.turnList) < 2):
            return None
        
        if(self.turnList[0] == self.turnList[1]): #if we have 2 L's or  R's
            # change the restricted turn based on our direction
            if self.turnList[0] == Direction.RIGHT:
                relativeTurn = "R"
            else:
                relativeTurn = "L"
                
            dir = None
            
            if(self.dir == Direction.LEFT):
                if relativeTurn == "R":
                    dir = Direction.UP
                else:
                    dir = Direction.DOWN
                    
            elif(self.dir == Direction.RIGHT):
                if relativeTurn == "R":
                    dir = Direction.DOWN
                else:
                    dir = Direction.UP
                    
            elif(self.dir == Direction.DOWN):
                if relativeTurn == "R":
                    dir = Direction.LEFT
                else:
                    dir = Direction.RIGHT
                    
            elif(self.dir == Direction.UP):
                if relativeTurn == "R":
                    dir = Direction.RIGHT
                else:
                    dir = Direction.LEFT
                    
            return dir
        
        return None
    def interpretTurns(self):
        turnList = list()
        if(len(self.turnHistory) >= 3):
            for i in range(0, 2):
                if(self.turnHistory[i] == Direction.LEFT):
                    if(self.turnHistory[i+1] == Direction.DOWN):
                        turnList.append(Direction.LEFT) #left turn
                    elif(self.turnHistory[i+1] == Direction.UP):
                        turnList.append(Direction.RIGHT) #right turn
                if(self.turnHistory[i] == Direction.RIGHT):
                    if(self.turnHistory[i+1] == Direction.UP):
                        turnList.append(Direction.LEFT) #left turn
                    elif(self.turnHistory[i+1] == Direction.DOWN):
                        turnList.append(Direction.RIGHT) #right turn
                if(self.turnHistory[i] == Direction.UP):
                    if(self.turnHistory[i+1] == Direction.LEFT):
                        turnList.append(Direction.LEFT) #left turn
                    elif(self.turnHistory[i+1] == Direction.RIGHT):
                        turnList.append(Direction.RIGHT) #right turn
                if(self.turnHistory[i] == Direction.DOWN):
                    if(self.turnHistory[i+1] == Direction.LEFT):
                        turnList.append(Direction.RIGHT) #right turn
                    elif(self.turnHistory[i+1] == Direction.RIGHT):
                        turnList.append(Direction.LEFT) #left turn
        return turnList
    def testTrails(self):   
        for y in range(100, 600, 5):
            x1 = 100
            x2 = 600
            self.trail.addBlock(x1,y)
            self.trail.addBlock(x2,y)
        for x in range(100, 600, 5):
            y = 100
            self.trail.addBlock(x,y)
            self.trail.addBlock(x,y+500)
    
    def randomDir(self):
        x = random.randint(0,4)
        dir = Direction.UP
        if(x == 0):
            dir = Direction.UP 
        elif(x == 1):
            dir = Direction.DOWN
        elif(x == 2):
            dir = Direction.LEFT 
        elif(x == 3):
            dir = Direction.RIGHT
            
        return dir
    def updateHitBoxes(self):
        self.hitBoxes["UP"] = pygame.Rect(self.x, self.y-self.width, self.width, self.width)
        self.hitBoxes["DOWN"] = pygame.Rect(self.x, self.y+self.width, self.width, self.width)
        self.hitBoxes["LEFT"] = pygame.Rect(self.x-self.width, self.y, self.width, self.width)
        self.hitBoxes["RIGHT"] = pygame.Rect(self.x+self.width, self.y, self.width, self.width)
        self.hitBoxes["STILL"] = pygame.Rect(self.x, self.y, self.width, self.width)
        self.hitBoxes["BIGUP"] = pygame.Rect(self.x, self.y-(self.width*2), self.width, self.width*2)
        self.hitBoxes["BIGDOWN"] = pygame.Rect(self.x, self.y+(self.width*2), self.width, self.width*2)
        self.hitBoxes["BIGLEFT"] = pygame.Rect(self.x-(self.width*2), self.y, self.width*2, self.width)
        self.hitBoxes["BIGRIGHT"] = pygame.Rect(self.x+(self.width*2), self.y, self.width*2, self.width)
        
    def chooseSideTurn(self):
        r = random.randint(0,1)
    
        if self.dir == Direction.UP or self.dir == Direction.DOWN:
            if r == 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        elif self.dir == Direction.LEFT or self.dir == Direction.RIGHT:
            if r == 0:
                return Direction.UP
            else:
                return Direction.DOWN
            
    def edgeTurn(self,thresh):
        if 0 < self.x < 800*thresh:
            if self.dir != Direction.LEFT:
                 if self.dir == Direction.UP or self.dir == Direction.DOWN:
                     return Direction.RIGHT
        
        if 0 < self.y < 750*thresh:
            if self.dir != Direction.UP:
                if self.dir == Direction.LEFT or self.dir == Direction.RIGHT:
                    return Direction.DOWN
        
        if self.x > 800-(800*thresh):
            if self.dir != Direction.RIGHT:
                if self.dir == Direction.UP or self.dir == Direction.DOWN:
                    return Direction.LEFT
        
        if self.y > 750-(750*thresh):
            if self.dir != Direction.DOWN:
                if self.dir == Direction.LEFT or self.dir == Direction.RIGHT:
                    return Direction.UP
        
            
        return self.dir
    def edgeCheck(self,thresh):
        if 0 < self.x < 800*thresh or 0 < self.y < 750*thresh or self.x > 800-(800*thresh) or self.y > 750-(750*thresh):
            return True
        
        return False
    

    def clear(self,x,y):
        self.trail = Trail(5, 5, self.color)
        self.x = x
        self.y = y
        
    def addBlock(self):
        
        center = pygame.Rect(self.rect).center
        self.trail.addBlock(center[0], center[1])
        
    def removeBlock(self):
        if(self.trail == None):
            return "STILL"
        self.trail.removeBlock()
    
    def collideBorders(self,width,height):
        if pygame.Rect(self.rect).top <= 0 or pygame.Rect(self.rect).bottom >= height or pygame.Rect(self.rect).left <= 0 or pygame.Rect(self.rect).right >= width:
            return True #if player collides with border, return true.
    
    def collideWithSelf(self):
        if(self.trail == None):
            return
        index = pygame.Rect(self.rect).collidelistall(self.trail.blocks) #return an index of the rect that collided with 
        for i in index:
            if(i < len(self.trail.blocks) - 10): # ignore the first 5 blocks closest to the player head 
                return True
        return False
    
    def checkHitBox(self, ourHB, player): #check collision of HB and Player Trials
        index = pygame.Rect(ourHB).collidelistall(player.trail.blocks) #return an index of the rect that collided with 
        for i in index:
            if(i < len(player.trail.blocks) - 10): # ignore the first 5 blocks closest to the player head 
                return True
        return False
    
    def collideWithOther(self,other): 
        if(other.trail == None):
            return
        index = pygame.Rect(self.rect).collidelistall(other.trail.blocks) #return an index of the rect that collided with 
        for i in index:
            if(i != -1): # ignore the first 5 blocks closest to the player head 
                return True
        return False
        
    def drawTrail(self, surface):
        if(self.trail == None):
            return
        self.trail.drawBlocks(surface)
        
    def drawHitBoxes(self, screen):
        for dir, hb in self.hitBoxes.items():
            #key = self.stringifyDir()
            #if(dir == key):
                hbImage = pygame.Surface([self.width, self.width])
                hbImage.fill(pygame.Color('White'))
                hitBox = pygame.Rect(hb)
                pos = (hitBox.x, hitBox.y)
                screen.blit(hbImage, pos)
    
    def collideWithWall(self, hitbox, dirStr, screen): # self player HB collides with BorderWall
        if(dirStr == "UP"): #TOP of Screen
            if hitbox.top < 0:
                return True
        elif(dirStr == "DOWN"): #BOT
            if hitbox.bottom >= 760:
                return True
        elif(dirStr == "LEFT"): #LEFT
            if hitbox.left < 0:
                return True
        elif(dirStr == "RIGHT"): #RIGHT
            if hitbox.right >= 810:
                return True
    
    
        
        return False
    
    def HBCollideWall(self, hitbox): # self player HB collides with BorderWall
        
        if hitbox.top < 0:
            return True
    
        if hitbox.bottom >= 760:
            return True
    
        if hitbox.left < 0:
            return True
    
        if hitbox.right >= 810:
            return True

        return False
        
        
    def stringifyDir(self):
        if(self.dir == None):
            return 
        key = str(self.dir).split(".")[1]
        return key
    
    def checkUpDown(self,player, isBig,c):
        newDir = self.dir
        prefix = ""
        if(isBig):
            prefix += "BIG"
            
        if self.dir == Direction.UP: #curr traveling UP/DOWN
            
            if self.checkHitBox(self.hitBoxes[prefix+"LEFT"],player) or self.HBCollideWall(self.hitBoxes[prefix+"LEFT"]) or self.checkHitBox(self.hitBoxes[prefix+"LEFT"],self):
                newDir = Direction.RIGHT
            elif self.checkHitBox(self.hitBoxes[prefix+"RIGHT"],player) or self.HBCollideWall(self.hitBoxes[prefix+"RIGHT"]) or self.checkHitBox(self.hitBoxes[prefix+"RIGHT"],self):
                newDir = Direction.LEFT
            else:
                if c == 1:
                    newDir = Direction.RIGHT
                else:
                    newDir = Direction.LEFT
                            
        elif self.dir == Direction.DOWN:
                    
            if self.checkHitBox(self.hitBoxes[prefix+"LEFT"],player)  or self.HBCollideWall(self.hitBoxes[prefix+"LEFT"]) or self.checkHitBox(self.hitBoxes[prefix+"LEFT"],self):
                newDir = Direction.RIGHT
            elif self.checkHitBox(self.hitBoxes[prefix+"RIGHT"],player) or self.HBCollideWall(self.hitBoxes[prefix+"RIGHT"]) or self.checkHitBox(self.hitBoxes[prefix+"RIGHT"],self):
                newDir = Direction.LEFT
            else:
                if c == 1:
                    newDir = Direction.RIGHT
                else:
                    newDir = Direction.LEFT
                    
        return newDir
                    
    def checkLeftRight(self,player,isBig,c):
        newDir = self.dir
        prefix = ""
        if(isBig):
            prefix += "BIG"
        
        
        if self.dir == Direction.LEFT: #Going LEFT/RIGHT rn 
                    
            if self.checkHitBox(self.hitBoxes[prefix+"UP"],player) or self.HBCollideWall(self.hitBoxes[prefix+"UP"]) or self.checkHitBox(self.hitBoxes[prefix+"UP"],self):
                newDir = Direction.DOWN
            elif self.checkHitBox(self.hitBoxes[prefix+"DOWN"],player) or self.HBCollideWall(self.hitBoxes[prefix+"DOWN"]) or self.checkHitBox(self.hitBoxes[prefix+"DOWN"],self):
                newDir = Direction.UP
            else:
                if c == 1:
                    newDir = Direction.UP
                else:
                    newDir = Direction.DOWN
                            
                    
        elif self.dir == Direction.RIGHT:
            
            if self.checkHitBox(self.hitBoxes[prefix+"UP"],player) or self.HBCollideWall(self.hitBoxes[prefix+"UP"]) or self.checkHitBox(self.hitBoxes[prefix+"UP"],self):
                newDir = Direction.DOWN
            elif self.checkHitBox(self.hitBoxes[prefix+"DOWN"],player) or self.HBCollideWall(self.hitBoxes[prefix+"DOWN"]) or self.checkHitBox(self.hitBoxes[prefix+"DOWN"],self):
                newDir = Direction.UP
            else:
                if c == 1:
                    newDir = Direction.UP
                else:
                    newDir = Direction.DOWN
        
        return newDir
    
    def AITurn(self, player, screen):
        dir = self.dir
        
        if self.dir != Direction.STILL:
            key = self.stringifyDir()
            ##print(key)
            hitBox = self.hitBoxes[key]
            ##print(key)
            c = random.randint(1,2)
            #check HB with enemy or ourself.
            
            if self.collideWithWall(hitBox, key, screen):
                if self.dir == Direction.UP or self.dir == Direction.DOWN:
                    if self.HBCollideWall(self.hitBoxes["LEFT"]):
                        dir = Direction.RIGHT
                    elif self.HBCollideWall(self.hitBoxes["RIGHT"]):
                        dir = Direction.LEFT
                    else:
                        if c == 1:
                            dir = Direction.RIGHT
                        else:
                            dir = Direction.LEFT
                            
                elif self.dir == Direction.LEFT or self.dir == Direction.RIGHT:
                    if self.HBCollideWall(self.hitBoxes["UP"]):
                        dir = Direction.DOWN
                    elif self.HBCollideWall(self.hitBoxes["DOWN"]):
                        dir = Direction.UP
                    
                    else:
                        if c == 1:
                            dir = Direction.UP
                        else:
                            dir = Direction.DOWN
            
            if(self.checkHitBox(hitBox, player) or (self.checkHitBox(hitBox, self))):
                ##print("About to collide with something, " + str(self.dir))
                newDir = None
                
                #if(self.dir == Direction.UP):
                    ##print("Going UP, should go " + str(self.checkUpDown(player,False, c)))
                    
                if self.checkUpDown(player,False, c) != dir:
                    ##print("CUD 1")
                    newDir = self.checkUpDown(player,False, c)
                elif self.checkUpDown(player,True, c) != dir:
                    ##print("CUD 2")
                    newDir = self.checkUpDown(player,True, c)
                elif self.checkLeftRight(player,False,c) != dir:
                    ##print("CLR 1")
                    newDir = self.checkLeftRight(player,False,c)
                else:
                    ##print("CLR 2")
                    newDir = self.checkLeftRight(player,True,c)
                            
                dir = newDir
                ##print("Choosing to go " + str(dir))
                
                        
        return dir
            
    def update(self, ticker):
        if self.dir == Direction.UP:
            self.y -= self.speed
        elif self.dir == Direction.DOWN:
            self.y += self.speed
        elif self.dir == Direction.LEFT:
            self.x -= self.speed
        elif self.dir == Direction.RIGHT:
            self.x += self.speed
        self.turnTimer -= ticker
        
        self.rect = (self.x, self.y, 20, 20)
        self.updateHitBoxes()
    
    def setDir(self, dir):
        self.dir = dir