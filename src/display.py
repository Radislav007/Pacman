import os
import pygame
import time

from src.settings import WIDTH, HEIGHT, CHAR_SIZE
from src.button import Button

class Display():
    def __init__(self, screen):
        self.screen = screen
        self.size = CHAR_SIZE
        self.font = pygame.font.Font(None, 36)
        self.x = 0
        self.y = HEIGHT

        # Абсолютний шлях до картинки pacman-2.png
        base_dir = os.path.dirname(os.path.abspath(__file__))  # шлях до папки src/
        assets_dir = os.path.join(base_dir, '..', 'assets')   # вихід з src/ до assets/
        image_path = os.path.join(assets_dir, 'pacman', 'pacman-2.png')
        
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        # Для додаткового лічильника очок, шрифт Arial 24 пікс.
        self.score_font = pygame.font.SysFont('Arial', 24)
        
    def show_life(self, life, screen):
        for i in range(life):
            screen.blit(self.image, (self.x + ( self.size *(i + 1)), self.y))
            
    def show_level(self, level, screen):
        text = self.font.render(f"Рівень: {level}", True, (255, 255, 255))
        screen.blit(text, (self.x + self.size, self.y + self.size))
        
    def show_score(self, score, screen):
        # Відображає очки у лівому нижньому куті, з урахуванням висоти екрану
        score_text = self.score_font.render(f"Рахунок: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, HEIGHT + 10))

    def show_timer(self, screen, text):
        background_width = WIDTH 
        background_height = HEIGHT 
        background_rect = pygame.Rect(0, 0, background_width, background_height)
        pygame.draw.rect(screen, (30, 30, 60), background_rect)  # темно-синій фон

        for i in range(3, 0, -1):
            timer_text = self.font.render(f"Гра почнеться через {i}", True, (255, 255, 255))
            main_text = self.font.render(f"{text}", True, (255, 255, 255))

            timer_rect = timer_text.get_rect(center=background_rect.center)
            main_text_rect = main_text.get_rect(center=background_rect.center)
            main_text_rect.move_ip(0, -self.size)
            
            screen.blit(timer_text, timer_rect)
            screen.blit(main_text, main_text_rect)

            pygame.display.flip()
            time.sleep(1)
            pygame.draw.rect(screen, (30, 30, 60), background_rect)  # темно-синій фон
            
    def show_pause(self, screen):
        text = self.font.render("Пауза. Натисніть 'P' щоб продовжити", True, (255, 255, 255))
        text2 = self.font.render("Натисніть 'M' щоб відкрити меню", True, (255, 255, 255))
        
        text_rect = text.get_rect()
        text2_rect = text2.get_rect()
        
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        text2_rect.center = (WIDTH // 2, (HEIGHT // 2) + 50)
        
        background_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (30, 30, 60), background_rect)  # темно-синій фон
        
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)

    def show_menu(self, screen, close_menu, change_background_color, background_color, change_walls_color, walls_color):
        background_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (30, 30, 60), background_rect)  # темно-синій фон

        play_button = Button("Грати", WIDTH // 2 - 135, HEIGHT // 2 - 50, 270, 50)
        change_walls_color_button = Button("Змінити колір стіни", WIDTH // 2 - 135, HEIGHT // 2 + 20, 270, 50)
        change_background_color_button = Button("Змінити колір фону", WIDTH // 2 - 135, HEIGHT // 2 + 90, 270, 50)

        play_button.draw(screen)
        change_walls_color_button.draw(screen)
        change_background_color_button.draw(screen)

        walls_color_rect = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 2 + 30, 30, 30)  
        pygame.draw.rect(screen, walls_color, walls_color_rect)  
        pygame.draw.rect(screen, (255, 255, 255), walls_color_rect, 2)  

        bg_color_rect = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 2 + 100, 30, 30)  
        pygame.draw.rect(screen, background_color, bg_color_rect)  
        pygame.draw.rect(screen, (255, 255, 255), bg_color_rect, 2)  

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    close_menu()
                if change_background_color_button.is_clicked(event.pos):
                    change_background_color()
                if change_walls_color_button.is_clicked(event.pos):
                    change_walls_color()

        pygame.display.update()
