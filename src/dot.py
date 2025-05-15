import pygame
from src.settings import DOT_COLOR

class Dot(pygame.sprite.Sprite):
    def __init__(self, row, col, size, is_power = False):
        super().__init__()
        self.size = size
        self.x = (row * self.size) + (size // 2)
        self.y = (col * self.size) + (size // 2)
        self.rate = self.size // 3 if is_power else self.size // 6 
        self.is_power = is_power
        
        self.rect = pygame.Rect(self.x - self.rate // 2, self.y - self.rate // 2, self.rate, self.rate)
        
    def draw(self, screen):
        pygame.draw.rect(screen, DOT_COLOR, self.rect)
        