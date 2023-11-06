# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 21:15:49 2023

@author: jaime
"""

import numpy as np
import random
import pygame
import sys
import math
import time

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


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
LIGHT_GREY = (211, 211, 211)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

number_of_moves=0
SQUARESIZE = 75
dificulty_Num = 2 #default value is easy(2)

selected_color = WHITE
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
input_text = ""
number_of_moves =0
winner = ""

screen = pygame.display.set_mode((width, height))

pygame.init()



def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    
    for r in range(ROW_COUNT - 1):
            for c in range(COLUMN_COUNT - 1):
            # Check if a 2x2 square with the same piece exists
                if board[r][c] == piece and board[r][c + 1] == piece and board[r + 1][c] == piece and board[r + 1][c + 1] == piece:
                    return True
        
    return False

    

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0
    

    for r in range(ROW_COUNT - 1):  # Iterate through rows, up to the second to last row
        for c in range(COLUMN_COUNT - 1):  # Iterate through columns, up to the second to last column
            window = [board[r][c], board[r][c+1], board[r+1][c], board[r+1][c+1]]
            score += evaluate_window(window, piece)
    return score

    

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board,backgroud_color,selected_color,RADIUS,height):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, backgroud_color, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, selected_color, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


#fuction used to draw the pallet for backgroud
def draw_squares(screen_width):
    square_size = screen_width//5
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

#fuction used to get the color that was clicked
def get_clicked_color(mouse_pos, screen_width):
    square_size = screen_width // 5  # Adjust the square size based on your menu layout
    squares_per_row = 4  # Number of squares per row
    
    for i, (color, name) in enumerate(colors):
        row = i // squares_per_row  # Calculate the current row
        col = i % squares_per_row  # Calculate the current column
        x = col * (square_size + 20) + 20
        y = row * (square_size + 20) + 70
        rect = pygame.Rect(x, y, square_size, square_size)
        if rect.collidepoint(mouse_pos):
            print(name)
            return color
    return (255, 255, 255)









# menu starts ############################################################

def menu():
    global selected_difficulty
    global input_text
    global dificulty_Num
    selected_difficulty = "Easy"   #Default value
    
    screen_width = 500
    screen_height = 400
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Enter User Name")
    
    
    title_rect = pygame.Rect(0, 0, screen_width, 50)
    input_rect = pygame.Rect(25,50 , screen_width//2, 50)
    play_rect = pygame.Rect(300,330 , screen_width//3, 50)
    
    # Radio button positions and sizes
    button_radius = 10
    button_spacing = 30
    button_y = 160
    
    
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    # Initialize difficulty choice
    selected_difficulty = None
    menu_open = True
    active_input = False

    
    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_open = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active_input = True
                elif play_rect.collidepoint(event.pos):
                    if input_text == "":
                        input_text="YOU"
                    menu_open = False
                else:
                    active_input = False
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if a difficulty button was clicked
                    if (screen_width // 2 - button_spacing) <= mouse_pos[0] <= (screen_width // 2 - button_spacing + button_radius * 2):
                        if button_y <= mouse_pos[1] <= (button_y + button_radius * 2):
                            selected_difficulty = "Impossible"
                            dificulty_Num=5
                            
                        elif button_y + button_spacing <= mouse_pos[1] <= (button_y + button_spacing + button_radius * 2):
                            selected_difficulty = "Hard"
                            dificulty_Num=4
                        elif button_y + 2 * button_spacing <= mouse_pos[1] <= (button_y + 2 * button_spacing + button_radius * 2):
                            selected_difficulty = "Medium"
                            dificulty_Num=3
                        elif button_y + 3 * button_spacing <= mouse_pos[1] <= (button_y + 3 * button_spacing + button_radius * 2):
                            selected_difficulty = "Easy"
                            dificulty_Num=2
                        elif button_y + 4 * button_spacing <= mouse_pos[1] <= (button_y + 4 * button_spacing + button_radius * 2):
                            selected_difficulty = "Super Easy"
                            dificulty_Num =1
            elif event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_BACKSPACE:
                        # Handle backspace key to remove characters
                        input_text = input_text[:-1]
                    else:
                        # Add typed character to input text
                        input_text += event.unicode
    
        screen.fill((0, 0, 0))
              
        if selected_difficulty == "Impossible":
            pygame.draw.circle(screen, green, (screen_width // 2 - button_spacing + button_radius, button_y + button_radius), button_radius)
        else:
            pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + button_radius), button_radius)
        
        
        if selected_difficulty == "Hard":
            pygame.draw.circle(screen, green, (screen_width // 2 - button_spacing + button_radius, button_y + button_spacing + button_radius), button_radius)
        else:
            pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + button_spacing + button_radius), button_radius)
        
        
        if selected_difficulty == "Medium":
            pygame.draw.circle(screen, green, (screen_width // 2 - button_spacing + button_radius, button_y + 2 * button_spacing + button_radius), button_radius)
        else:
            pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + 2 * button_spacing + button_radius), button_radius)
        
        
        if selected_difficulty == "Easy":
            pygame.draw.circle(screen, green, (screen_width // 2 - button_spacing + button_radius, button_y + 3 * button_spacing + button_radius), button_radius)
        else:
            pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + 3 * button_spacing + button_radius), button_radius)
            
        if selected_difficulty == "Super Easy":
            pygame.draw.circle(screen, green, (screen_width // 2 - button_spacing + button_radius, button_y + 4 * button_spacing + button_radius), button_radius)
        else:
            pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + 4 * button_spacing + button_radius), button_radius)
        
        pygame.draw.rect(screen, (0,0,0), title_rect)
        pygame.draw.rect(screen, (0,255,0), play_rect)
       
        pygame.draw.rect(screen, (255,255,255), input_rect)
        #pygame.draw.rect(screen, (255,255,255), dificulty_rect_text)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Enter your name", True, (255, 255, 255))  # White text
        play_text = font.render("PLAY", True, (0, 0, 0))  # White text
        difficulty_text = font.render("Dificulty", True, (255, 255, 255))
        text_user = font.render(input_text, True, black)
        screen.blit(title_text, (20, 10))  # Position the title text
        screen.blit(difficulty_text, (20, 150))
        screen.blit(text_user, (27, 50))
        screen.blit(play_text, (310, 335))
    
        
    #    # Draw radio buttons and labels
    #    pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + button_radius), button_radius)
    #    pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + button_spacing + button_radius), button_radius)
    #    pygame.draw.circle(screen, white, (screen_width // 2 - button_spacing + button_radius, button_y + 2 * button_spacing + button_radius), button_radius)
    
        font = pygame.font.Font(None, 24)
        hard_text = font.render("Hard", True, white)
        medium_text = font.render("Medium", True, white)
        easy_text = font.render("Easy", True, white)
        super_easy_text = font.render("Super Easy", True, white)
        impossible_text = font.render("Impossible", True, white)
        screen.blit(impossible_text, (screen_width // 2 - button_spacing + button_radius * 3, button_y))
        screen.blit(hard_text, (screen_width // 2 - button_spacing + button_radius * 3, button_y + button_spacing))
        screen.blit(medium_text, (screen_width // 2 - button_spacing + button_radius * 3, button_y + 2 * button_spacing))
        screen.blit(easy_text, (screen_width // 2 - button_spacing + button_radius * 3, button_y + 3 * button_spacing))
        screen.blit(super_easy_text, (screen_width // 2 - button_spacing + button_radius * 3, button_y + 4 * button_spacing))
    
        pygame.display.flip()
        print("Selected Difficulty:", selected_difficulty)
        print("user name:", input_text)


def choose_bk_color():
    screen_width = 500
    screen_height = 600
    # Screen dimensions for backgroud color menu and square size
    
    
    title_rect = pygame.Rect(0, 0, screen_width, 50) # title for pick a color rect
    
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Color Selection Menu")
    menu2_open = True
    
    #menu color selection
    while menu2_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    return get_clicked_color(mouse_pos,screen_width)
                    
    
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0,0,0), title_rect)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Choose a Board Color", True, (255, 255, 255))  # White text
        screen.blit(title_text, (20, 10))  # Position the title text
        draw_squares(screen_width)
        pygame.display.flip()

def choose_first_player(input_text):
    WIDTH, HEIGHT = 500, 400
    # Initialize the screen for choose a player screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Player Choice")
    
    
    ai_button = pygame.draw.rect(screen, (0, 128, 255), (WIDTH // 5, HEIGHT // 2, 150, 50))
    player_button = pygame.draw.rect(screen, (0, 128, 255), (WIDTH // 5+ 160, HEIGHT // 2, 150, 50))
    
    player_choice_open = True
    
    while player_choice_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on a button
                if ai_button.collidepoint(event.pos):
                    return "AI"
                    player_choice_open= False
                elif player_button.collidepoint(event.pos):
                    return input_text
                    
    
        screen.fill(BLACK)
        #draw_text("Choose the player with the first move:", WIDTH // 2, HEIGHT // 3, (0, 0, 0))
    
        pygame.draw.rect(screen, WHITE, ai_button)
        pygame.draw.rect(screen, WHITE, player_button)
        font = pygame.font.Font(None, 36)
        move_title = font.render("FIRST MOVE", True, WHITE)
        AI_text = font.render("AI", True, BLACK)
        player_name_text = font.render(input_text, True, BLACK)
        
        screen.blit(move_title, (WIDTH//3, 20))
        screen.blit(AI_text,(WIDTH //5 + 5, HEIGHT//2 +5))
        screen.blit(player_name_text,(WIDTH // 5+ 165, HEIGHT // 2 + 5) )
        
    
        pygame.display.update()


#actual game starts######################################################

def play_game(selected_player):
    
    
    board = create_board()
    
    print_board(board)
    global dificulty_Num
    global input_text
    global number_of_moves
    global winner
    
    myfont = pygame.font.SysFont("monospace", 50)
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE
    size = (width, height)
    RADIUS = int(SQUARESIZE/2 - 5)
    game_over = False
    screen = pygame.display.set_mode((width, height))
    
    if selected_player=="AI":
        turn = AI
    else:
        turn = PLAYER
    
    
    
    screen = pygame.display.set_mode(size)
    draw_board(board,LIGHT_GREY,selected_color,RADIUS,height)
    pygame.display.update()
    print("dif"+ str (dificulty_Num))
    
    while not game_over:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                
    
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, LIGHT_GREY, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2)), RADIUS)
    
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
    
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
    
                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render(input_text +" wins!!", 1, WHITE)
                            screen.blit(label, (40,10))
                            game_over = True
                            winner = input_text
    
                        turn += 1
                        turn = turn % 2
                        number_of_moves +=1
    
                        print_board(board)
                        draw_board(board,LIGHT_GREY,selected_color,RADIUS,height)
    
    
        # # Ask for Player 2 Input
        if turn == AI and not game_over:                
    
            #col = random.randint(0, COLUMN_COUNT-1)
            #col = pick_best_move(board, AI_PIECE)
            availableColumns = get_valid_locations(board)
            col2, minimax_score = minimax(board, dificulty_Num, -math.inf, math.inf, True)
            
            if dificulty_Num == 1:
                if random.random() < 0.7:
                    # Choose a random column
                    col2 = random.choice(availableColumns)
                else:
                    # Use the Minimax algorithm
                    col2, minimax_score = minimax(board, dificulty_Num, -math.inf, math.inf, False)
            elif dificulty_Num == 2:
                if random.random() < 0.6:
                    col2 = random.choice(availableColumns)
                else:
                    col2, minimax_score = minimax(board, dificulty_Num, -math.inf, math.inf, False)
            elif dificulty_Num == 3:
                if random.random() < 0.4:
                    col2 = random.choice(availableColumns)
                else:
                    col2, minimax_score = minimax(board, dificulty_Num, -math.inf, math.inf, False)
            elif dificulty_Num == 4:
                if random.random() < 0.2:
                    col2 = random.choice(availableColumns)
                else:
                    col2, minimax_score = minimax(board, dificulty_Num, -math.inf, math.inf, False)
            else:
                col2, minimax_score = minimax(board, dificulty_Num, -math.inf, math.inf, False)
                
                
            
                
            
    
            if is_valid_location(board, col2):
                #pygame.time.wait(500)
                row = get_next_open_row(board, col2)
                drop_piece(board, row, col2, AI_PIECE)
    
                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player2 wins!!", 1, WHITE)
                    winner = "Player2"
                    screen.blit(label, (40,10))
                    game_over = True
                    
    
                print_board(board)
                draw_board(board,LIGHT_GREY,selected_color,RADIUS,height)
    
                turn += 1
                turn = turn % 2
                number_of_moves +=1
    
        if game_over:
            pygame.time.wait(3000)
            
            
def draw_text(text, x, y, color):
    FONT = pygame.font.Font(None, 36)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
    
def game_over_screen(winner, num_moves, total_time):
    global width
    global height
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    pygame.display.set_caption("Game Over")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_text("Game Over", width // 2, height // 4, (255, 0, 0))
        draw_text(f"Winner: {winner}", width // 2, height // 2, (255, 255, 255))
        draw_text(f"Number of Moves: {num_moves}", width // 2, height // 2 + 50, (255, 255, 255))
        draw_text(f"Total Time: {minutes}:{seconds} minutes", width // 2, height // 2 + 100, (255, 255, 255))

        pygame.display.update()




def main():
    global selected_color
    global input_text
    global winner
    global number_of_moves

    menu()
    selected_color = choose_bk_color()
    chosen_player = choose_first_player(input_text)
    
    start_time = time.time()
    play_game(chosen_player)
    end_time = time.time()
    final_time = end_time-start_time
    game_over_screen(winner,number_of_moves,round(final_time,0))
    pygame.quit()
    sys.exit()
if __name__ =="__main__":
    main()