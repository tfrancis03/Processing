import pygame
from Block import Block


class Trail():
    
    def __init__(self, width, height, color):
        
        self.width = width
        self.height = height
        self.color = color
        self.blocks = []
        self.blockGroup = pygame.sprite.Group()
        
    def addBlock(self, x, y): #add a new block to list of blocks
        block = Block(x,y,self.width,self.height,self.color)
        self.blockGroup.add(block)
        self.blocks.append(block)

    
    def removeBlock(self): #removes the oldest block from trails
        if(len(self.blocks) == 0):
            return 
        self.blockGroup.remove(self.blocks.pop(0))
    
    def drawBlocks(self, surface):
        self.blockGroup.draw(surface)
        