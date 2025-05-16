import pygame

class Button:
    def __init__(self, text, x, y, width, height, font_size=36):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.text_surf = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
