# Імпортуємо модулі
import pygame  # Бібліотека для створення ігор
import sys     # Для завершення програми
import argparse  # Для роботи з аргументами командного рядка

# Імпортуємо власні модулі
from src.settings import WIDTH, HEIGHT, MARGIN_BOTTOM
from src.game import Game
from src.colors import COLORS  # Імпорт кольорів з окремого файлу

class Main:
    def __init__(self, fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + MARGIN_BOTTOM))
        pygame.display.set_caption("PacMan")
        self.clock = pygame.time.Clock()
        self.fps = fps

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
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            if not game.is_pause:
                game.update()

            pygame.display.update()
            self.clock.tick(self.fps)

def parse_arguments():
    parser = argparse.ArgumentParser(description="PacMan Game")
    parser.add_argument('--fps', type=int, default=30, help='FPS (кадрів на секунду)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    main = Main(fps=args.fps)
    main.start()
