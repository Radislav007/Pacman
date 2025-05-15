import pygame
from src.settings import MAP, CHAR_SIZE
from src.tile import Tile
from src.dot import Dot
from src.ghost import Ghost
from src.pacman import Pacman
from src.display import Display

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background_colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.walls_colors = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.current_background_color_index = 0
        self.current_walls_color_index = 0
        
        self.background_color = self.background_colors[self.current_background_color_index]
        self.walls_color = self.walls_colors[self.current_walls_color_index]
        
        self.pacman = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.dots = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.is_menu_open = True
        self.is_pause = False 
        self.power_mode_duration = 5000
        self.power_mode_start_time = None

        self.display = Display(self.screen)

        self.game_over = False
        self.power_mode = False
        self.level = 1
        self.score = 0

        self.collect_game()


    def collect_game(self, collect_type='start_over', life=3, level=1): 
        def clear():
            self.pacman = pygame.sprite.GroupSingle()
            self.ghosts = pygame.sprite.Group()
            self.walls = pygame.sprite.Group()

        if collect_type == 'new_level':
            self.display.show_timer(self.screen, 'Ви переходите на новий рівень')
            clear()
            self.dots = pygame.sprite.Group()
            self.pacman.sprite = Pacman(0, 0, CHAR_SIZE, life)

        elif collect_type == 'start_over':
            self.is_menu_open = True
            clear()
            self.dots = pygame.sprite.Group()
            self.level = 1
            self.score = 0
            self.pacman.sprite = Pacman(0, 0, CHAR_SIZE, life)  

        elif collect_type == 'remove_life':
            self.display.show_timer(self.screen, 'Вас зїли')
            clear()
            self.pacman.sprite = Pacman(0, 0, CHAR_SIZE, life)

        for y, col in enumerate(MAP):
            for x, el in enumerate(col):
                if el == '1':
                    self.walls.add(Tile(x, y, CHAR_SIZE,  self.walls_color))
                elif el == '.':
                    if collect_type != 'remove_life':
                        self.dots.add(Dot(x, y, CHAR_SIZE))
                elif el == 'B':
                    if collect_type != 'remove_life':
                        self.dots.add(Dot(x, y, CHAR_SIZE, is_power=True))
                elif el == 'b':
                    self.ghosts.add(Ghost(x, y, CHAR_SIZE, 'blinky', level))
                elif el == 'c':
                    self.ghosts.add(Ghost(x, y, CHAR_SIZE, 'clyde', level))
                elif el == 'i':
                    self.ghosts.add(Ghost(x, y, CHAR_SIZE, 'inky', level))
                elif el == 'p':
                    self.ghosts.add(Ghost(x, y, CHAR_SIZE, 'pinky', level))
                elif el == 'P':
                    self.pacman.add(Pacman(x, y, CHAR_SIZE, self.pacman.sprite.life))

        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]

    def close_menu(self):
        self.is_menu_open = False

    def change_background_color(self):
        self.current_background_color_index = (self.current_background_color_index + 1) % len(self.background_colors)
        self.background_color = self.background_colors[self.current_background_color_index]
        
    def change_walls_color(self):
        self.current_walls_color_index = (self.current_walls_color_index + 1) % len(self.walls_colors)
        self.walls_color = self.walls_colors[self.current_walls_color_index]
        for wall in self.walls:
            wall.update_color(self.walls_color)
        
    def draw(self):
        self.screen.fill(self.background_color)
        if self.is_pause:
            self.display.show_pause(self.screen)
        elif self.is_menu_open:
            self.display.show_menu(self.screen, self.close_menu, self.change_background_color, self.background_color, self.change_walls_color, self.walls_color)
        else:
            pressed_key = pygame.key.get_pressed()

            if self.power_mode:
                current_time = pygame.time.get_ticks()
                if current_time - self.power_mode_start_time > self.power_mode_duration:
                    self.power_mode = False

            if len(self.dots) == 0:
                self.level += 1
                self.collect_game('new_level', self.pacman.sprite.life, self.level)

            for dot in self.dots:
                if self.pacman.sprite.rect.colliderect(dot.rect):
                    if dot.is_power:
                        self.power_mode = True
                        self.score += 50
                        self.power_mode_start_time = pygame.time.get_ticks()
                    else:
                        self.score += 10
                    dot.kill()

            for ghost in self.ghosts:
                if self.pacman.sprite.rect.colliderect(ghost.rect):
                    if self.power_mode:
                        ghost.move_to_start()
                    else:
                        self.pacman.sprite.life -= 1
                        if self.pacman.sprite.life == 0:
                            self.collect_game('start_over')
                        else:
                            self.collect_game('remove_life', self.pacman.sprite.life)

            [wall.draw(self.screen) for wall in self.walls.sprites()]
            [dot.draw(self.screen) for dot in self.dots.sprites()]
            [ghost.update(self.walls_collide_list, self.power_mode) for ghost in self.ghosts]
            self.ghosts.draw(self.screen)

            self.pacman.sprite.move(pressed_key, self.walls_collide_list)
            self.pacman.draw(self.screen)

            self.display.show_life(self.pacman.sprite.life, self.screen)
            self.display.show_level(self.level, self.screen)
            self.display.show_score(self.score, self.screen)

