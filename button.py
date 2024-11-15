import pygame
import sys


BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0, 170, 250)
DARK_BLUE = (0, 143, 250)
GREEN = (0,128,128)
DARK_GREN = (0,102,128)
RED = (200,20,0)
DARK_RED= (136,20,0)
GRAY =(100,100,100)


class Button:
    def __init__(self, x, y, width, height, text, active, color=RED, hover_color=DARK_RED):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text       
        self.current_color = color
        self.font = pygame.font.SysFont("Arial",14)
        self.active = active
        self.color = color
        self.hover_color = hover_color
        

    def draw(self, screen):
        # Change color when hovered
        if self.active:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        else:           
            self.current_color = GRAY
            self.hover_color = GRAY     

        pygame.draw.rect(screen, self.current_color, self.rect,border_radius=10)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False