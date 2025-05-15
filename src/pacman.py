import pygame

from src.settings import PACMAN_SPEED, WIDTH

class Pacman(pygame.sprite.Sprite):
    def __init__(self, row, col, size, life = 3):
        super().__init__()
        self.size = size
        self.x = row * self.size
        self.y = col * self.size
        self.speed = PACMAN_SPEED
        self.life = life
        
        self.frames = [
            pygame.image.load("assets/pacman/pacman-1.png"),
            pygame.image.load("assets/pacman/pacman-2.png"),
            pygame.image.load("assets/pacman/pacman-3.png"),
            pygame.image.load("assets/pacman/pacman-4.png"),
        ]
        self.frames = [pygame.transform.scale(frame, (self.size, self.size)) for frame in self.frames]
        
        self.frame_index = 0 
        self.frame_speed = 5 
        self.frame_counter = 0 
        
        
        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        
        self.keys = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
        }
        
        self.directions = {
            'left': (-self.speed, 0),
            'right': (self.speed, 0),
            'up': (0, -self.speed),
            'down': (0, self.speed),
        }
        
        self.direction = (0, 0)
        self.direction_name = ''
        
        
    def move_to_start(self):
        self.rect.x = self.x
        self.rect.y = self.y
        
    def is_collide(self, x, y, walls_collide_list):
        rect = self.rect.move(x, y)
        
        if rect.collidelist(walls_collide_list) == -1:
            return False
        return True
        
    def animate_pacman(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.rotate_pacman()

        
    def rotate_pacman(self):
        if self.direction_name == "right":
            self.image = self.frames[self.frame_index]
        elif self.direction_name == "left":
            self.image = pygame.transform.rotate(self.frames[self.frame_index], 180) 
        elif self.direction_name == "up":
            self.image = pygame.transform.rotate(self.frames[self.frame_index], 90)  
        elif self.direction_name == "down":
            self.image = pygame.transform.rotate(self.frames[self.frame_index], -90) 
            
            
    def move(self, pressed_key, walls_collide_list):
        for key, value in self.keys.items():
        
            if pressed_key[value] and not self.is_collide(*self.directions[key], walls_collide_list):
                self.direction = self.directions[key]
                self.direction_name = key
                break  
            elif self.is_collide(*self.direction, walls_collide_list):
                self.direction = (0, 0)
              
        
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0
            
        self.animate_pacman()
        self.rect.move_ip(self.direction)
                