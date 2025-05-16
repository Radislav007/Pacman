import pygame

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, size, is_power=False):
        super().__init__()
        self.size = size
        self.is_power = is_power
        self.alive = True  # додано

        # Завантаження зображення або малювання крапки
        if self.is_power:
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((255, 255, 0))  # наприклад, жовта крапка для бонусу
        else:
            self.image = pygame.Surface((self.size // 3, self.size // 3))
            self.image.fill((255, 255, 255))  # звичайна біла крапка

        self.rect = self.image.get_rect(topleft=(x * size + size // 3, y * size + size // 3))

    def update(self, pacman):
        if self.alive and self.rect.colliderect(pacman.rect):
            self.kill()
            self.alive = False
