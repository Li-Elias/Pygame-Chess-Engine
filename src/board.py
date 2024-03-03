from constants import *
from pieces import *
from squares import Square


class Board:
    
    def __init__(self) -> None:
        self.history = []
        self.valid_moves = []
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.convert_to_fen()
        self.current_piece = None
        self.status = "KQkq -"
        self.halfmove_counter = 0
        self.fullmove_counter = 1
    
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    
    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
        
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        
        
    def square_valid(self, row, col):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
        
        
    def calculate_moves(self, row, col, piece):
        '''
            Calculate all the valid moves of a specific piece on a specific position
        '''      
        
        def _pawn_moves():
            if piece.color == "black":
                all_pawn_move_moves = ((row+1, col), (row+2, col)) if not piece.moved else ((row+1, col),)
                all_pawn_attack_moves = ((row+1, col+1), (row+1, col-1))
            else:
                all_pawn_move_moves = ((row-1, col), (row-2, col+0)) if not piece.moved else ((row-1, col),)
                all_pawn_attack_moves = ((row-1, col+1), (row-1, col-1))


            for move in all_pawn_move_moves:
                move_row = move[0]
                move_col = move[1]
                
                if self.square_valid(move_row, move_col):
                    if not self.squares[move_row][move_col].has_piece():
                        self.valid_moves.append(move)
                    else: break
                        
            for move in all_pawn_attack_moves:
                move_row = move[0]
                move_col = move[1]
                
                if self.square_valid(move_row, move_col):
                    if self.squares[move_row][move_col].has_enemy_piece(piece.color): # or self.en_passant((move_row, move_col)):
                        self.valid_moves.append(move)
        
        
        def _knight_moves():
            available_knight_moves = (
                (row+2, col+1), # top right
                (row+2, col-1), # top left
                (row-2, col+1), # bottom right
                (row-2, col-1), # bottom left
                (row+1, col+2), # right top
                (row-1, col+2), # right bottom
                (row+1, col-2), # left top
                (row-1, col-2), # left bottom
            )
            
            for move in available_knight_moves:
                move_row = move[0]
                move_col = move[1]
                
                if self.square_valid(move_row, move_col):
                    if not self.squares[move_row][move_col].has_team_piece(piece.color):
                        self.valid_moves.append(move)                       
                    
        
        def _bishop_moves():
            available_bishop_moves = (
                (1, 1), # top right
                (1, -1), # top left
                (-1, 1), # bottom right
                (-1, -1), # bottom left
            )
            
            for move in available_bishop_moves:
                for i in range(1, 7):          
                    move_row = row + move[0] * i
                    move_col = col + move[1] * i
                    
                    if not self.square_valid(move_row, move_col):
                        break
                    elif self.squares[move_row][move_col].has_team_piece(piece.color):
                        break
                    elif self.squares[move_row][move_col].has_enemy_piece(piece.color):                     
                        self.valid_moves.append((move_row, move_col))
                        break
                    else: self.valid_moves.append((move_row, move_col))
                        
        
        def _rook_moves():
            available_rook_moves = (
                (1, 0), # top
                (-1, 0), # bottom
                (0, 1), # right
                (0, -1), # left
            )
            
            for move in available_rook_moves:
                for i in range(1, 7):          
                    move_row = row + move[0] * i
                    move_col = col + move[1] * i
                    
                    if not self.square_valid(move_row, move_col):
                        break
                    elif self.squares[move_row][move_col].has_team_piece(piece.color):
                        break
                    elif self.squares[move_row][move_col].has_enemy_piece(piece.color):                     
                        self.valid_moves.append((move_row, move_col))
                        break
                    else: self.valid_moves.append((move_row, move_col))
                        
        
        def _queen_moves():
            available_queen_moves = (
                (1, 0), # top
                (-1, 0), # bottom
                (0, 1), # right
                (0, -1), # left
                (1, 1), # top right
                (1, -1), # top left
                (-1, 1), # bottom right
                (-1, -1), # bottom left
            )
            
            for move in available_queen_moves:
                for i in range(1, 7):          
                    move_row = row + move[0] * i
                    move_col = col + move[1] * i
                    
                    if not self.square_valid(move_row, move_col):
                        break
                    elif self.squares[move_row][move_col].has_team_piece(piece.color):
                        break
                    elif self.squares[move_row][move_col].has_enemy_piece(piece.color):                     
                        self.valid_moves.append((move_row, move_col))
                        break
                    else: self.valid_moves.append((move_row, move_col))
                        
                
        def _king_moves():
            available_king_moves = (
                (row+1, col+0), # top
                (row-1, col+0), # bottom
                (row+0, col+1), # right
                (row+0, col-1), # left
                (row+1, col+1), # top right
                (row+1, col-1), # top left
                (row-1, col+1), # bottom right
                (row-1, col-1), # bottom left
            )
            
            for move in available_king_moves:
                move_row = move[0]
                move_col = move[1]
                
                if not self.square_valid(move_row, move_col):
                    continue    
                elif self.squares[move_row][move_col].has_team_piece(piece.color):
                    continue
                elif self.squares[move_row][move_col].has_enemy_piece(piece.color):
                    self.valid_moves.append(move)
                    continue
                else: self.valid_moves.append(move)
                
                
        def _castling_moves():
            castling_kingside = True
            castling_queenside = True
            
            for j in range(1, 2):
                if self.squares[row][col+j].has_piece():
                    castling_kingside = False
                    
            for j in range(1, 3):
                if self.squares[row][col-j].has_piece():
                    castling_queenside = False
            
            if castling_kingside == True and not piece.moved:
                self.valid_moves.append((row, col+2))
                
            if castling_queenside == True and not piece.moved:
                self.valid_moves.append((row, col-2))
                    
        
        self.current_piece = (row, col)            
        
        if piece.name == "pawn":
            _pawn_moves()
        elif piece.name == "knight":
            _knight_moves()
        elif piece.name == "bishop":
            _bishop_moves()
        elif piece.name == "rook":
            _rook_moves()
        elif piece.name == "queen":
            _queen_moves()
        elif piece.name == "king":
            _king_moves()
            _castling_moves()
            
            
    #def en_passant(self, move):
    #    if self.squares[self.current_piece[0]][self.current_piece[1]].is_empty():
    #        return False
    #    
    #    if self.squares[self.current_piece[0]][self.current_piece[1]].piece.name != "pawn":
    #        return False
    #    
    #    transmutation_table = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    #    part = self.status.split(" ")[1]
    #    
    #    if part != "-":
    #        return (7-int(part[1])+1, transmutation_table[part[0]]) == move
    #    else:
    #        return False
    

    def validate_move(self, move_to_validate, castling="no"):
        piece = self.squares[self.current_piece[0]][self.current_piece[1]].piece
        if castling == "no": self.take_move(move_to_validate[0], move_to_validate[1])
        current_piece = self.current_piece
        targetet_squares = []
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_enemy_piece(piece.color):
                    self.calculate_moves(row, col, self.squares[row][col].piece)
                    targetet_squares = targetet_squares + self.valid_moves
                    self.valid_moves.clear()
                elif self.squares[row][col].has_specific_team_piece("king", piece.color) and castling == "no":
                    king_pos = (row, col)
                    
        if castling == "no": self.undo_move()
        self.current_piece = current_piece

        if castling == "no": return True if king_pos not in targetet_squares else False
        else:
            row = self.current_piece[0]
            col = self.current_piece[1]
            
            if castling == "king":
                squares_to_check = [(row, col+1), (row, col+2)]
            if castling == "queen":
                squares_to_check = [(row, col-1), (row, col-2), (row, col-3)]    
                
            for square in squares_to_check:
                if square in targetet_squares:
                    return False
            return True
    
    
    def calculate_valid_moves(self, row, col, piece):
        self.calculate_moves(row, col, piece)
        moves_to_validate = self.valid_moves.copy()
        valid_moves = []
        cp_row = self.current_piece[0]
        cp_col = self.current_piece[1]
        
        for move_to_validate in moves_to_validate:
            if move_to_validate == (cp_row, cp_col+2) and piece.name == "king":
                if self.validate_move(move_to_validate, "king"):
                    valid_moves.append(move_to_validate)
            elif move_to_validate == (cp_row, cp_col-2) and piece.name == "king":
                if self.validate_move(move_to_validate, "queen"):
                    valid_moves.append(move_to_validate)
                    
            elif self.validate_move(move_to_validate):
                valid_moves.append(move_to_validate)
    
        self.valid_moves = valid_moves.copy()
    

    def convert_to_fen(self):
        transmutation_table = {"whitepawn": "P",
                               "whiteknight": "N",
                               "whitebishop": "B",
                               "whiterook": "R",
                               "whitequeen": "Q",
                               "whiteking": "K",
                               "blackpawn": "p",
                               "blackknight": "n",
                               "blackbishop": "b",
                               "blackrook": "r",
                               "blackqueen": "q",
                               "blackking": "k"}
        
        fen_string = ""
        count = 0
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    name = self.squares[row][col].piece.name
                    color = self.squares[row][col].piece.color
                    piece = color + name
                    if count == 0: fen_string = fen_string + transmutation_table[piece]
                    else: fen_string = fen_string + str(count) + transmutation_table[piece]
                    count = 0
                else: count += 1
            if count != 0: fen_string = fen_string + str(count)
            if row != 7: fen_string = fen_string + "/"
            count = 0
        
        self.history.append(fen_string)
        
        
    def load_fen_string(self, fen_string):
        transmutation_table = {"P": "white",
                               "N": "white",
                               "B": "white",
                               "R": "white",
                               "Q": "white",
                               "K": "white",
                               "p": "black",
                               "n": "black",
                               "b": "black",
                               "r": "black",
                               "q": "black",
                               "k": "black"}
        
        row = 0
        col = 0
        
        self._create()
        
        for letter in fen_string:
            if letter == "/":
                row += 1
                col = 0
            elif letter in transmutation_table:
                if letter.lower() == "p":
                    self.squares[row][col].piece = Pawn(transmutation_table[letter])
                    
                    if letter.isupper() and row != 6:
                        self.squares[row][col].piece.moved = True
                    elif letter.islower() and row != 1:
                        self.squares[row][col].piece.moved = True
                        
                elif letter.lower() == "n":
                    self.squares[row][col].piece = Knight(transmutation_table[letter])
                elif letter.lower() == "b":
                    self.squares[row][col].piece = Bishop(transmutation_table[letter])
                elif letter.lower() == "r":
                    self.squares[row][col].piece = Rook(transmutation_table[letter])
                elif letter.lower() == "q":
                    self.squares[row][col].piece = Queen(transmutation_table[letter])
                elif letter.lower() == "k":
                    self.squares[row][col].piece = King(transmutation_table[letter])
                    
                    if letter.isupper() and row != 7 and col != 4:
                        self.squares[row][col].piece.moved = True
                    elif letter.islower() and row != 0 and col != 4:
                        self.squares[row][col].piece.moved = True
                
                col += 1
            else:
                col += int(letter)
                
    
    def take_computer_move(self, move, move_sound, capture_sound):
        transmutation_table = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        
        piece_pos = move[:2]
        destination_pos = move[2:]
        
        if self.squares[7-int(destination_pos[1])+1][transmutation_table[destination_pos[0]]].has_piece():
            capture_sound.play()
            self.halfmove_counter = 0
        else: 
            move_sound.play()
            self.halfmove_counter += 1
        
        self.current_piece = (7-int(piece_pos[1])+1, transmutation_table[piece_pos[0]])
        self.take_move(7-int(destination_pos[1])+1, transmutation_table[destination_pos[0]])
        
        self.convert_to_fen()
                
                
    def take_move(self, row, col):
        old_row = self.current_piece[0]
        old_col = self.current_piece[1]
        piece = self.squares[old_row][old_col].piece
        piece.moved = True
      
        self.squares[old_row][old_col].piece = None
        self.squares[row][col].piece = piece
        
        # castling
        if piece.name == "king":
            if (row, col) == (old_row, old_col+2):
                rook = self.squares[row][7].piece
                self.squares[row][col-1].piece = rook
                self.squares[row][7].piece = None
                
                string = ""
                status = self.status.split(" ")
                for letter in status[0]:
                    if letter.islower():
                        string = string + letter
                self.status = f"{string} {status[1]}"
                
            elif (row, col) == (old_row, old_col-2):
                rook = self.squares[row][0].piece
                self.squares[row][col+1].piece = rook
                self.squares[row][0].piece = None
                
                string = ""
                status = self.status.split(" ")
                for letter in status[0]:
                    if letter.isupper():
                        string = string + letter
                self.status = f"{string} {status[1]}"
                
        ## en passant
        #elif piece.name == "pawn":
        #    if old_row - row == 2 or old_row - row == -2:
        #        transmutation_table = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        #        parts = self.status.split(" ")
        #        r = 7-row if piece.color == "white" else 7-row+2
        #        string = f"{parts[0]} {transmutation_table[col]}{r}"
        #        self.status = string
        #    elif self.en_passant((row, col)):
        #        if piece.color == "white": self.squares[row+1][col].piece = None
        #        else: self.squares[row-1][col].piece = None
        #        parts = self.status.split(" ")
        #        string = f"{parts[0]} -"
        #        
        #    
        #    # promotion
        #    elif row == 7:
        #        self.squares[row][col].piece = Queen(piece.color)
                
        self.convert_to_fen() 
    
    
    def undo_move(self):
        if len(self.history) != 1:
            self.history.pop(-1)

        self.load_fen_string(self.history[-1])
