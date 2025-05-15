import pygame
import sys
import argparse
from src.settings import WIDTH, HEIGHT, MARGIN_BOTTOM
from src.game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + MARGIN_BOTTOM))
pygame.display.set_caption('Pacman')

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}

class Main:
    def __init__(self, screen, background_color, walls_color):
        self.screen = screen
        self.FPS = pygame.time.Clock()
        self.initial_background_color = background_color
        self.initial_walls_color = walls_color

    def start(self):
        game = Game(self.screen)
        
        if self.initial_background_color:
            while game.background_color != self.initial_background_color:
                game.change_background_color()
        if self.initial_walls_color:
            while game.walls_color != self.initial_walls_color:
                game.change_walls_color()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game.is_pause = not game.is_pause
                    if event.key == pygame.K_m:
                        game.is_pause = False
                        game.is_menu_open = True
                        
            if not game.is_pause:
                game.draw() 
            else:
                game.display.show_pause(self.screen)

            pygame.display.update()
            self.FPS.tick(30)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Pacman Game with customizable colors')
    parser.add_argument('--background', type=str, choices=COLORS.keys(), default='black',
                        help='Set the initial background color (default: black)')
    parser.add_argument('--walls', type=str, choices=COLORS.keys(), default='white',
                        help='Set the initial walls color (default: white)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    
    background_color = COLORS[args.background]
    walls_color = COLORS[args.walls]
    
    play = Main(screen, background_color, walls_color)
    play.start()