# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 22:12:21 2023

@author: jaime
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 01:22:08 2023

@author: jaime
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 400
WHITE = (255, 255, 255)
BLACK = (0,0,0)

input_text ="Jaime"

# Initialize the screen for choose a player screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))



def draw_text(text, x, y, color):
    FONT = pygame.font.Font(None, 36)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
    
def game_over_screen(winner, num_moves, total_time):
    pygame.display.set_caption("Game Over")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_text("Game Over", WIDTH // 2, HEIGHT // 4, (255, 0, 0))
        draw_text(f"Winner: {winner}", WIDTH // 2, HEIGHT // 2, (255, 255, 255))
        draw_text(f"Number of Moves: {num_moves}", WIDTH // 2, HEIGHT // 2 + 50, (255, 255, 255))
        draw_text(f"Total Time: {total_time} minutes", WIDTH // 2, HEIGHT // 2 + 100, (255, 255, 255))

        pygame.display.update()
def main():
    # Example usage
    winner = "Player 1"
    num_moves = 42
    total_time = 120.5
    game_over_screen(winner, num_moves, total_time)

if __name__ == "__main__":
    main()