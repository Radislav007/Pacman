import pygame

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 0))  # Жовта крапка
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True  # Крапка активна

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)

    def update(self, pacman):
        if self.alive and self.rect.colliderect(pacman.rect):
            self.kill()
            self.alive = False

