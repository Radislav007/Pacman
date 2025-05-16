import os
import pygame

from src.settings import PACMAN_SPEED, WIDTH

class Pacman(pygame.sprite.Sprite):
    def __init__(self, row, col, size, life=3):
        super().__init__()
        self.size = size
        self.x = row * self.size
        self.y = col * self.size
        self.speed = PACMAN_SPEED
        self.life = life

        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, '..', 'assets', 'pacman')

        # frames для кожного напрямку (4 кадри анімації для кожного напрямку)
        # Потрібно мати 4 папки: left, right, up, down або іншим чином організувати,
        # Але якщо нема, то просто відображаємо як було, без поворотів
        self.frames = [
            pygame.image.load(os.path.join(assets_dir, "pacman-1.png")),
            pygame.image.load(os.path.join(assets_dir, "pacman-2.png")),
            pygame.image.load(os.path.join(assets_dir, "pacman-3.png")),
            pygame.image.load(os.path.join(assets_dir, "pacman-4.png")),
        ]
        self.frames = [pygame.transform.scale(frame, (self.size, self.size)) for frame in self.frames]

        self.frame_index = 0
        self.frame_speed = 5  # кадр змінюємо кожні 5 оновлень
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

        self.direction_name = None
        self.direction = (0, 0)

    def move(self, pressed_key, walls_collide_list):
        dx, dy = 0, 0
        moved = False

        for dir_name, key in self.keys.items():
            if pressed_key[key]:
                dx, dy = self.directions[dir_name]
                self.direction_name = dir_name
                moved = True
                break  # рух лише в одному напрямку за раз

        new_rect = self.rect.move(dx, dy)
        if moved and new_rect.collidelist(walls_collide_list) == -1:
            self.rect = new_rect

            # Оновлення анімації при русі
            self.frame_counter += 1
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
        else:
            # Якщо не рухаємось або зіткнення — показуємо "відкритий рот" (перший кадр)
            self.frame_index = 0
            self.frame_counter = 0
            self.image = self.frames[self.frame_index]

        # телепортація при виході за межі екрану по горизонталі
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
