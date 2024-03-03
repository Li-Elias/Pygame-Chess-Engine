import pygame
import sys
import random
import time

from stockfish import Stockfish

from constants import *
from game import Game
from button import Button
from server import Server
from client import Client


class Main:
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        self.game = Game()
        
    
    def mainloop(self):
        pygame.display.set_caption("Menu")
        
        screen = self.screen
        
        while True:
            screen.fill((240, 240, 240))
            
            PLAY_BUTTON = Button(None, (600, 525), "PLAY", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            OPTIONS_BUTTON = Button(None, (600, 675), "OPTIONS", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            
            # get mouse pos
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            
            for button in [PLAY_BUTTON, OPTIONS_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                # click buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.game_select()
                    elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                        
            pygame.display.update()
            
    
    def game_select(self):
        pygame.display.set_caption("Select gamemode")
                 
        screen = self.screen
        
        while True:
            screen.fill((240, 240, 240))
            
            SINGLEPLAYER_BUTTON = Button(None, (600, 425), "SINGLEPLAYER", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            MULTIPLAYER_BUTTON = Button(None, (600, 600), "MULTIPLAYER", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            LOCAL_GAME_BUTTON = Button(None, (600, 775), "LOCAL", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            
            # get mouse pos
            GAME_SELECT_MOUSE_POS = pygame.mouse.get_pos()
        
            for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, LOCAL_GAME_BUTTON]:
                button.changeColor(GAME_SELECT_MOUSE_POS)
                button.update(screen)
                
            for event in pygame.event.get():
                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # return to menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.main()
                    
                # click buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SINGLEPLAYER_BUTTON.checkForInput(GAME_SELECT_MOUSE_POS):
                        self.singleplayer()
                    elif MULTIPLAYER_BUTTON.checkForInput(GAME_SELECT_MOUSE_POS):
                        self.select_multiplayer_mode()           
                    elif LOCAL_GAME_BUTTON.checkForInput(GAME_SELECT_MOUSE_POS):
                        self.local_game()        
            
            pygame.display.update()
            
            
    def options(self):
        pygame.display.set_caption("Options")
                 
        screen = self.screen
        
        while True:
            screen.fill((240, 240, 240))
            
            RESULUTION_BUTTON = Button(None, (600, 600), "Resulution", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            
            # get mouse pos
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            
            for button in [RESULUTION_BUTTON]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(screen)
                
            for event in pygame.event.get():
                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # return to menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.main()
                    
                # click buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESULUTION_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
                
            pygame.display.update()
            
    
    def select_multiplayer_mode(self):
        pygame.display.set_caption("Select mode for multiplayer")
                        
        screen = self.screen
                        
        while True:
            screen.fill((240, 240, 240))

            SERVER_BUTTON = Button(None, (600, 525), "SERVER", Button.get_font(125), (200, 200, 200), (210, 210, 210))
            CLIENT_BUTTON = Button(None, (600, 675), "CLIENT", Button.get_font(125), (200, 200, 200), (210, 210, 210))
                            
            # get mouse pos
            MULTIPLAYER_MOUSE_POS = pygame.mouse.get_pos()

            for button in [SERVER_BUTTON, CLIENT_BUTTON]:
                button.changeColor(MULTIPLAYER_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # return to game_select    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_select()

                # click buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SERVER_BUTTON.checkForInput(MULTIPLAYER_MOUSE_POS):
                        self.multiplayer(server_user=True)
                    elif CLIENT_BUTTON.checkForInput(MULTIPLAYER_MOUSE_POS):
                        self.multiplayer()
                        
            pygame.display.update()
                        
    
    def singleplayer(self):
        pygame.display.set_caption("Singleplayer")

        screen = self.screen
        game = self.game
        board = self.game.board
        
        stockfish = Stockfish(path=fr"{PATH}\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2")
        stockfish.set_elo_rating(STOCKFISH_ELO)
        
        value = random.randint(0, 1)
        player_color = "white" if value == 0 else "black"
        computer_color = "black" if value == 0 else "white"
        
        while True:
            # show board
            game.show_bg(screen)
            game.show_pieces(screen)
            game.show_moves(screen)

            for event in pygame.event.get():
                # quit application    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # return to game_select    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_select()
                    
                # click
                elif event.type == pygame.MOUSEBUTTONDOWN and game.next_player == player_color:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_row = mouse_pos[1] // SQSIZE
                    clicked_col = mouse_pos[0] // SQSIZE
                    
                    # calculate valid moves
                    if board.squares[clicked_row][clicked_col].has_team_piece(game.next_player):
                        board.valid_moves.clear()
                        board.current_piece = None
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calculate_valid_moves(clicked_row, clicked_col, piece)
                    
                    # take move
                    elif (clicked_row, clicked_col) in board.valid_moves:
                        if board.squares[clicked_row][clicked_col].has_enemy_piece(game.next_player): #or board.en_passant((clicked_row, clicked_col)):
                            game.config.capture_sound.play()
                            board.halfmove_counter = 0
                        else:
                            game.config.move_sound.play()
                            board.halfmove_counter += 1
                        
                        board.take_move(clicked_row, clicked_col)
                        board.valid_moves.clear()
                        board.current_piece = None
                        
                        if game.next_player == "white":
                            game.next_player = "black"
                        else:
                            game.next_player = "white"
                            board.fullmove_counter += 1
                        
                
                # reaction from computer
                elif game.next_player == computer_color:
                    fen_position = f"{board.history[-1]} {game.next_player[0]} {board.status} {board.halfmove_counter} {board.fullmove_counter}"
                    stockfish.set_fen_position(fen_position)
                    best_move = stockfish.get_best_move()
                    board.take_computer_move(best_move, game.config.move_sound, game.config.capture_sound)
                    
                    if game.next_player == "white":
                        game.next_player = "black"
                    else:
                        game.next_player = "white"
                        board.fullmove_counter += 1

            pygame.display.update()
    
    
    def multiplayer(self, server_user=False):
        pygame.display.set_caption("Multiplayer")
        
        # initialize Sever and Client
        if server_user is True:
            server = Server(SERVER_IP, PORT)
        client = Client(SERVER_IP, PORT)
        
        screen = self.screen
        game = self.game
        board = self.game.board
    
        player_color = client.send_data("COLOR")
        
        while True:
            # show board
            game.show_bg(screen)
            game.show_pieces(screen)
            game.show_moves(screen)

            for event in pygame.event.get():
                # quit application   
                if event.type == pygame.QUIT:
                    if server_user is True:
                        server.close()
                    client.close()
                    pygame.quit()
                    sys.exit()
                
                # return to game_select    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if server_user is True:
                        server.close()
                    client.close()
                    self.game_select()
                    
                if game.next_player == player_color:
                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_row = mouse_pos[1] // SQSIZE
                        clicked_col = mouse_pos[0] // SQSIZE

                        # calculate valid moves
                        if board.squares[clicked_row][clicked_col].has_team_piece(game.next_player):
                            board.valid_moves.clear()
                            board.current_piece = None
                            piece = board.squares[clicked_row][clicked_col].piece
                            board.calculate_valid_moves(clicked_row, clicked_col, piece)

                        # take move
                        elif (clicked_row, clicked_col) in board.valid_moves:
                            if board.squares[clicked_row][clicked_col].has_enemy_piece(game.next_player): #or board.en_passant((clicked_row, clicked_col)):
                                game.config.capture_sound.play()
                                board.halfmove_counter = 0
                            else:
                                game.config.move_sound.play()
                                board.halfmove_counter += 1

                            board.take_move(clicked_row, clicked_col)
                            board.valid_moves.clear()
                            board.current_piece = None

                            if game.next_player == "white":
                                game.next_player = "black"
                            else:
                                game.next_player = "white"
                                board.fullmove_counter += 1

                            client.send_data(f"{board.history[-1]} {game.next_player[0]} {board.status} {board.halfmove_counter} {board.fullmove_counter}")
                    
                # waiting for respone
                else:
                    s_time = time.time()
                    
                    # waiting for reaction 
                    while client.send_data("REQUEST_POSITION") == f"{board.history[-1]} {game.next_player[0]} {board.status} {board.halfmove_counter} {board.fullmove_counter}":
                        passed_time = time.time() - s_time
                        pygame.display.set_caption("Multiplayer: Waiting for respone..." + str(round(passed_time)))
                    
                    # recieves information from server
                    fen_string = client.send_data("REQUEST_POSITION").split()
                    
                    print(fen_string)
                    
                    board.load_fen_string(fen_string[0])
                    board.history.append(fen_string[0])
                    game.next_player = "black" if fen_string[1] == "b" else "white"
                    board.status = f"{fen_string[2]} {fen_string[3]}"
                    board.halfmove_counter = int(fen_string[4])
                    board.fullmove_counter = int(fen_string[5])
                    
                    pygame.display.set_caption("Multiplayer")
                        
            pygame.display.update()
            
                        
    def local_game(self):
        pygame.display.set_caption("Local Game")

        screen = self.screen
        game = self.game
        board = self.game.board
        
        while True:
            # show board
            game.show_bg(screen)
            game.show_pieces(screen)
            game.show_moves(screen)

            for event in pygame.event.get():
                # quit application    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # return to game_select    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_select()
                    
                # click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_row = mouse_pos[1] // SQSIZE
                    clicked_col = mouse_pos[0] // SQSIZE
                    
                    # calculate valid moves
                    if board.squares[clicked_row][clicked_col].has_team_piece(game.next_player):
                        board.valid_moves.clear()
                        board.current_piece = None
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calculate_valid_moves(clicked_row, clicked_col, piece)
                    
                    # take move
                    if (clicked_row, clicked_col) in board.valid_moves:
                        if board.squares[clicked_row][clicked_col].has_enemy_piece(game.next_player): # or board.en_passant((clicked_row, clicked_col)):
                            game.config.capture_sound.play()
                            board.halfmove_counter = 0
                        else:
                            game.config.move_sound.play()
                            board.halfmove_counter += 1
                        
                        board.take_move(clicked_row, clicked_col)
                        board.valid_moves.clear()
                        board.current_piece = None
                        
                        if game.next_player == "white":
                            game.next_player = "black"
                        else:
                            game.next_player = "white"
                            board.fullmove_counter += 1
                        
            pygame.display.update()
            
            
if __name__ == "__main__":
    main = Main()
    main.mainloop()
    