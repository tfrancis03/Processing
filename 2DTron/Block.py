import pygame

class Block(pygame.sprite.Sprite):

    image = None

    
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color(color))
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.centerx = x
        self.rect.top = y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)