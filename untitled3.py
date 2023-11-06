# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 00:03:28 2023

@author: jaime
"""
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 500
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 200
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



game_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 1, 0, 1, 1]
]

print(score_position(game_board,2))