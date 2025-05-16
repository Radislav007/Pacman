import pygame
from src.settings import DOT_COLOR

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, size, is_power=False):
        super().__init__()
        self.is_power = is_power
        self.size = size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        if self.is_power:
            pygame.draw.circle(self.image, (255, 255, 0), (size // 2, size // 2), size // 2)  # Жовта велика крапка
        else:
            # Використовуємо DOT_COLOR, як було у HEAD (припускаю, що це білий)
            pygame.draw.circle(self.image, DOT_COLOR, (size // 2, size // 2), size // 6)  # Крапка кольору з налаштувань

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * size + size // 2 - self.rect.width // 2,
                             y * size + size // 2 - self.rect.height // 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
