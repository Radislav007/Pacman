import os
import pygame
import random

from src.settings import GHOST_SPEED, WIDTH

class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, size, ghost_name, level):
        super().__init__()
        self.level = level
        self.size = size
        self.x = row * self.size
        self.y = col * self.size
        self.ghost_name = ghost_name
        self.speed = GHOST_SPEED
        
        self.move_dir = 'up'
        
        # Визначаємо абсолютний шлях до папки assets
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, '..', 'assets', self.ghost_name)
        self.img_path = os.path.join(assets_dir, f'{self.move_dir}.png')
        
        self.image = pygame.image.load(self.img_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        self.keys = ['left', 'right', 'up', 'down']
        self.directions = {
            'left': (-self.speed, 0),
            'right': (self.speed, 0),
            'up': (0, -self.speed),
            'down': (0, self.speed),
        }
        self.direction = (0, 0)
        
    def move_to_start(self):
        self.rect.x = self.x
        self.rect.y = self.y
        
    def is_collide(self, x, y, walls_collide_list):
        rect = self.rect.move(x, y)
        
        if rect.collidelist(walls_collide_list) == -1:
            return False
        return True
        
        
    def animate(self, power_mode):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if power_mode:
            self.img_path = os.path.join(base_dir, '..', 'assets', 'edible', 'ghost.png')
        else:
            assets_dir = os.path.join(base_dir, '..', 'assets', self.ghost_name)
            self.img_path = os.path.join(assets_dir, f'{self.move_dir}.png')
            
        self.image = pygame.image.load(self.img_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
          
    def update(self, walls_collide_list, power_mode):
        available_moves = []
        
        for key in self.keys:
            if not self.is_collide(*self.directions[key], walls_collide_list):
                available_moves.append(key)
        
        is_random = False if len(available_moves) <= 2 and self.direction != (0, 0) else True
        
        if is_random and random.randrange(0, 100) <= 30 + (self.level * 3):
            self.move_dir = random.choice(available_moves)
            self.direction = self.directions[self.move_dir]

        if not self.is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)
    
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0
        
        self.animate(power_mode)
