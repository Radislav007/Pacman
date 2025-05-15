# Імпортуємо модулі
import pygame  # Бібліотека для створення ігор
import sys     # Для завершення програми

# Імпортуємо власні модулі
from src.settings import WIDTH, HEIGHT, MARGIN_BOTTOM, FPS

from src.game import Game
from src.colors import COLORS  # Імпорт кольорів з окремого файлу
from src.utils import draw_text  # Імпорт функції для малювання тексту

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + MARGIN_BOTTOM))
        pygame.display.set_caption("PacMan")
        self.clock = pygame.time.Clock()
        self.fps = FPS

    def start(self):
        game = Game(self.screen)
        game.draw_board()
        game.draw_enemies()
        game.draw_player()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print("Pause toggled")
                        game.is_pause = not game.is_pause
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        print("Pressed: UP")
                    elif event.key == pygame.K_DOWN:
                        print("Pressed: DOWN")
                    elif event.key == pygame.K_LEFT:
                        print("Pressed: LEFT")
                    elif event.key == pygame.K_RIGHT:
                        print("Pressed: RIGHT")

            if not game.is_pause:
                game.update()
            else:
                draw_text(self.screen, "PAUSE", (WIDTH // 2, HEIGHT // 2), size=60)

            pygame.display.update()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    main = Main()
    main.start()
