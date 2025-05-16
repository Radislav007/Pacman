import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, row, col, size, color):
        super().__init__()
        self.size = size
        self.x = row * self.size
        self.y = col * self.size
        self.color = color
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def update_color(self, new_color):
        self.color = new_color