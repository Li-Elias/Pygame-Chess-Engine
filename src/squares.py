
class Square:
    
    def __init__(self, row, col, piece=None) -> None:
        self.row = row
        self.col = col
        self.piece = piece
        
    
    def has_piece(self):
        return self.piece != None
    
    
    def is_empty(self):
        return self.piece == None
    
    
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    
    def has_specific_team_piece(self, name, color):
        return self.has_piece() and self.piece.color == color and self.piece.name == name 
    