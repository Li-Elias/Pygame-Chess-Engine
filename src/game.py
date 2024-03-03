import pygame

from constants import *
from config import Config
from board import Board


class Game:
    
    def __init__(self) -> None:
        self.next_player = 'white'
        self.checkmate = False
        self.config = Config()
        self.board = Board()
    
    
    def show_bg(self, surface):
        theme = self.config.theme
        
        count = 0
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if count % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                count += 1
                
            # since theres an even number of squares go back one value
            count -= 1
            
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    rect = (col * SQSIZE, row * SQSIZE)
                    img = pygame.transform.scale(piece.texture, (SQSIZE, SQSIZE))
                    surface.blit(img, rect)
                    
    
    def show_moves(self, surface):
        theme = self.config.theme
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        if self.board.current_piece is not None:
            original_row, original_col = self.board.current_piece
        
            for move in self.board.valid_moves:      
                row = move[0]
                col = move[1]

                img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2

                # if enemy piece can be captured or not
                if self.board.squares[row][col].has_enemy_piece(self.board.squares[original_row][original_col].piece.color):
                    pygame.draw.circle(screen, theme.move, img_center, SQSIZE // 2, 13)
                else:
                    pygame.draw.circle(screen, theme.move, img_center, SQSIZE // 6)

                surface.blit(screen, (0, 0))
                    