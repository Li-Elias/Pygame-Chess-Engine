import os
import pygame

from constants import *


class Piece:
    
    def __init__(self, name, color, value, texture=None) -> None:
        self.name = name
        self.color = color
        self.value = value
        self.texture = texture
        self.moved = False
        self.set_texture()
        
    
    def set_texture(self):
        self.texture = pygame.image.load(os.path.join(
            f"{PATH}/assets/images/standard_{self.color}_{self.name}.png"))
        
        
class Pawn(Piece):
    def __init__(self, color):
        super().__init__("pawn", color, 1.0)
        
        
class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color, 3.05)
        
        
class Bishop(Piece):
    def __init__(self, color):
        super().__init__("bishop", color, 3.33)
        
        
class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color, 5.63)
        
class Queen(Piece):
    def __init__(self, color):
        super().__init__("queen", color, 9.5)
        
        
class King(Piece):
    def __init__(self, color):
        super().__init__("king", color, float("inf"))
        