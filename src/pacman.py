import os
import pygame

from src.settings import PACMAN_SPEED, WIDTH

class Pacman(pygame.sprite.Sprite):
    def __init__(self, row, col, size, life=3):
        super().__init__()
        self.size = size
        self.start_x = row * self.size
        self.start_y = col * self.size
        self.x = self.start_x
        self.y = self.start_y
        self.speed = PACMAN_SPEED
        self.life = life

        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, '..', 'assets', 'pacman')

        self.frames = [
            pygame.image.load(os.path.join(assets_dir, "pacman-1.png")),
            pygame.image.load(os.path.join(assets_dir, "pacman-2.png")),
            pygame.image.load(os.path.join(assets_dir, "pacman-3.png")),
            pygame.image.load(os.path.join(assets_dir, "pacman-4.png")),
        ]
        self.frames = [pygame.transform.scale(frame, (self.size, self.size)) for frame in self.frames]

        self.frame_index = 0
        self.frame_speed = 5
        self.frame_counter = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

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

        self.direction_name = ''
        self.direction = (0, 0)

    def move(self, pressed_key, walls_collide_list):
        dx, dy = 0, 0
        for dir_name, key in self.keys.items():
            if pressed_key[key]:
                dx, dy = self.directions[dir_name]
                self.direction_name = dir_name
                break  # тільки один напрямок за раз

        new_rect = self.rect.move(dx, dy)
        if new_rect.collidelist(walls_collide_list) == -1:
            self.rect = new_rect

            # Оновлення анімації
            self.frame_counter += 1
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
        else:
            # Якщо зіткнення — скидаємо анімацію
            self.frame_index = 0
            self.frame_counter = 0
            self.image = self.frames[self.frame_index]

        # Телепортація при виході за край екрану
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0

    def reset_position(self):
        """Повертає Pacman на початкову позицію"""
        self.rect.topleft = (self.start_x, self.start_y)
        self.frame_index = 0
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
