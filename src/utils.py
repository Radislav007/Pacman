import pygame

def draw_text(screen, text, position, size=30, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=position)
    screen.blit(rendered, rect)
