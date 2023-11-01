# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 22:59:29 2023

@author: jaime
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors and color names
colors = [
    ((230, 219, 172), "Tan"),
    ((238, 220, 154), "Beige"),
    ((249, 224, 118), "Macaroon"),
    ((201, 187, 142), "Hazel Wood"),
    ((221, 184, 90), "Granola"),
    ((223, 201, 138), "Oat"),
    ((250, 226, 156), "Egg Nog"),
    ((200, 169, 81), "Fawn"),
    ((243, 234, 175), "Sugar Cookie"),
    ((216, 184, 99), "Sand"),
    ((227, 183, 120), "Sepia"),
    ((231, 194, 125), "Latte"),
    ((220, 215, 160), "Oyster"),
    ((227, 197, 101), "Biscotti"),
    ((253, 233, 146), "Parmesan"),
    ((189, 165, 93), "Hazelnut")
]


# Screen dimensions and square size
real_screen_height = 600
screen_width = 500
screen_height = 400
square_size = screen_width//5

# Create the Pygame screen
screen = pygame.display.set_mode((screen_width, real_screen_height))
pygame.display.set_caption("Color Selection Menu")

def draw_squares():
    
    squares_per_row = 4  # Number of squares per row
    
    for i, (color, name) in enumerate(colors):
        
        row = i // squares_per_row  # Calculate the current row
        col = i % squares_per_row  # Calculate the current column
        x = col * (square_size + 20) + 20
        y = row * (square_size + 20) + 70
        pygame.draw.rect(screen, color, (x, y, square_size, square_size))
        font = pygame.font.Font(None, 12)
        text = font.render(name, True, (253, 253, 253))
        screen.blit(text, (x + 10, y + square_size + 5))


def get_clicked_color(mouse_pos):
    for i, (color, name) in enumerate(colors):
        x = (i % 5) * (square_size + 20) + 20
        y = (i // 5) * (square_size + 20) + 20
        rect = pygame.Rect(x, y, square_size, square_size)
        if rect.collidepoint(mouse_pos):
            return name
    return None


title_rect = pygame.Rect(0, 0, screen_width, 50)


    
selected_color = None

menu_open = True


while menu_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_open = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                selected_color = get_clicked_color(mouse_pos)
                menu_open = False  # Exit the menu when a color is selected

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0,0,0), title_rect)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Choose a Background Color", True, (255, 255, 255))  # White text
    screen.blit(title_text, (20, 10))  # Position the title text
    draw_squares()
    pygame.display.flip()

pygame.quit()

if selected_color:
    print(f"Selected color: {selected_color}")
