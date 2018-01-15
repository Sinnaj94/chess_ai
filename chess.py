import numpy as np
import math
import Tkinter as tk
import string
import csv
import emoji


class GameManager:
    def __init__(self):
        self.board = Board()
        self.board.reset_board()
        self.interface = CUI(self.board)
        self.game_logic = GameLogic(self.board)
        self.board.set_player_names(self.interface.get_player_names())
        self.game_loop()

    def game_loop(self):
        current_player = self.board.player1
        while True:
            self.interface.output_board()
            self.interface.output_player(current_player)
            vector = [[None, None],[None, None]]
            while not self.game_logic.get_valid_position(vector[0]):
                vector[0] = self.interface.get_position(False)
            while not self.game_logic.get_valid_position(vector[1]):
                vector[1] = self.interface.get_position(True)
            print vector
            # Naechster Player ist am Zug.
            current_player = self.get_next_player(current_player)

    def get_next_player(self, current_player):
        if current_player == self.board.player1:
            return self.board.player2
        elif current_player == self.board.player2:
            return self.board.player1
        return None

    def get_figure_by_string(self, string):
        ascii = string.ascii_lowercase


class GameLogic:
    def __init__(self, board):
        self.board = board

    def selected_piece_belongs_to_player(self, piece, player):
        return piece.owner == player

    def get_piece_on_position(self, position):
        for piece in self.board.pieces:
            if piece.x == position[0] and piece.y == position[1]:
                return piece
        return False

    def get_valid_position(self, position):
        if 0 <= position[0] <= self.board.my_size and 0 <= position[1] < self.board.my_size:
            return True
        return False


class Interface:
    def __init__(self, board):
        self.board = board

    def output_board(self):
        raise NotImplementedError

    def output_player(self, player):
        raise NotImplementedError

    """
    Returns position as a vector.
    """
    def get_position(self, end):
        raise NotImplementedError

    def get_player_names(self):
        raise NotImplementedError



class CUI(Interface):
    def __init__(self, board):
        Interface.__init__(self, board)
        self.rendered = self.board.field
        self.asciis = string.ascii_lowercase

    def get_player_names(self):
        names = ["Player 1", "Player 2"]
        names[0] = raw_input("Bitte Namen von Spieler eins angeben:")
        names[1] = raw_input("Bitte Namen von Spieler zwei angeben:")
        return names

    def get_position(self, end):
        my_return = None
        if not end:
            my_return = str(raw_input("Bitte Startpunkt angeben (a1-h8):"))
        else:
            my_return = str(raw_input("Bitte Endpunkt angeben (a1-h8):"))
        formatted = self.convert_to_position(my_return)
        if not formatted:
            self.get_position(end)
        return formatted

    def convert_to_position(self, my_input):
        pos = []
        try:
            pos.append(int(ord(my_input[0])-97))
            pos.append(int(my_input[1])-1)
            return pos
        except (ValueError, IndexError) as e:
            return False

    def output_player(self, player):
        print player.name + " ist dran."

    def output_board(self):
        self.generate_board()
        self.render_board()

    def generate_board(self):
        for piece in self.board.pieces:
            self.rendered[piece.y][piece.x] = piece.character
        return self.rendered

    def render_board(self):
        for i_row in range(len(self.rendered)):
            printed = str(i_row+1)
            for i_column in range(len(self.rendered[i_row])):
                printed += " " + str(self.rendered[i_row][i_column])
            print printed
        letters = " "
        for i_letter in range(len(self.rendered)):
            letters += " " + self.asciis[i_letter]
        print letters


class Configuration:
    def __init__(self):
        self.input_file = "./configuration.csv"

    def get_configuration(self):
        input = []
        with open(self.input_file, 'rb') as conf:
            reader = csv.reader(conf)
            for row in reader:
                input.append(row)
        return input


class Board:
    def __init__(self):
        self.my_size = 8
        self.field = np.chararray((self.my_size, self.my_size))
        self.field[:] = '0'
        self.configuration = Configuration()
        self.pieces = []
        self.player1 = Player("Player 1", False)
        self.player2 = Player("Player 2", True)

    # see if the position is possible on the field or not
    def move_possible(self, x, y):
        return 0 <= x < self.my_size and 0 <= y < self.my_size

    def get_field(self):
        return self.field

    def set_player_names(self, player_names):
        self.player1.name = player_names[0]
        self.player2.name = player_names[1]

    def reset_board(self):
        conf = self.configuration.get_configuration()
        for row in range(0, len(conf)):
            for column in range(0, len(conf[row])):
                current_elem = conf[row][column]
                current_piece = self.create_piece(column, row, current_elem)
                if current_piece is not None:
                    self.add_piece(current_piece)
        return self.pieces

    def create_piece(self, x, y, char):
        # todo: Groesse checken und jeweilig davon machen
        if char=="t":
            return Tower(x, y, self.player2)
        elif char=="T":
            return Tower(x, y, self.player1)
        elif char=="s":
            return Springer(x, y, self.player2)
        elif char=="S":
            return Springer(x, y, self.player1)
        elif char=="b":
            return Bishop(x, y, self.player2)
        elif char=="B":
            return Bishop(x, y, self.player1)
        elif char=="k":
            return King(x, y, self.player2)
        elif char=="K":
            return King(x, y, self.player1)
        elif char=="q":
            return Queen(x, y, self.player2)
        elif char=="Q":
            return Queen(x, y, self.player1)
        elif char=="p":
            return Pawn(x, y, self.player2)
        elif char=="P":
            return King(x, y, self.player1)

    def add_piece(self, piece):
        self.pieces.append(piece)


class Player:
    def __init__(self, name, inverted):
        self.name = name
        # indicator, if player is on another site.
        self.inverted = inverted


#TODO: Pieces auslagern.
class Piece:
    def __init__(self, x, y, character, owner):
        self.x = x
        self.y = y
        if not character:
            self.character = "1"
        else:
            self.character = character
        self.owner = owner
        self.symbol = "x"

    def own_move_possibilities(self):
        return [0,0]

    def print_me(self):
        print self.character + " at " + str(self.x) + ", " + str(self.y)


class Pawn(Piece):
    def __init__(self, x, y, owner):
        Piece.__init__(self, x, y, "P", owner)

    # delta of move possibilities
    def own_move_possibilities(self):
        if self.y == 1:
            return [0, 1],[0, 2]
        return [0, 1]


class Tower(Piece):
    def __init__(self, x, y, owner):
        Piece.__init__(self, x, y, "T", owner)


class Springer(Piece):
    def __init__(self, x, y, owner):
        Piece.__init__(self, x, y, "S", owner)


class Bishop(Piece):
    def __init__(self, x, y, owner):
        Piece.__init__(self, x, y, "B", owner)


class King(Piece):
    def __init__(self, x, y, owner):
        Piece.__init__(self, x, y, "K", owner)


class Queen(Piece):
    def __init__(self, x, y, owner):
        Piece.__init__(self, x, y, "Q", owner)

game_manager = GameManager()
