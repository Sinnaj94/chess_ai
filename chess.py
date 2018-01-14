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
        while True:
            self.interface.output_board()
            self.interface.output_player(None)
            start = self.interface.get_position(False)
            # TODO: ueberpruefen
            end = self.interface.get_position(True)
            # TODO: ueberpruefen

    def get_figure_by_string(self, string):
        ascii = string.ascii_lowercase


class GameLogic:
    def __init__(self, board):
        self.board = board

    def selected_piece_belongs_to_player(self, piece, player):
        return piece.owner == player

    def get_piece_on_position(self):
        raise NotImplementedError


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


class CUI(Interface):
    def __init__(self, board):
        Interface.__init__(self, board)
        self.rendered = self.board.field
        self.asciis = string.ascii_lowercase

    def get_position(self, end):
        my_return = None
        if not end:
            my_return = str(raw_input("Bitte Startpunkt angeben (a1-h8):"))
        else:
            my_return = str(raw_input("Bitte Endpunkt angeben (a1-h8):"))
        return my_return

    def validate_input(self, my_input):
        first_char = False


    def validate_char(self, character):
        for i in range(self.board.my_size):
            if character == self.asciis[i]:
                return i
        return False

    def validate_number(self, number):
        if int()

    def output_player(self, player):
        #TODO
        print "Spieler ist dran."

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
        self.player1 = Player("Me", False)
        self.player2 = Player("Bot", True)

    # see if the position is possible on the field or not
    def move_possible(self, x, y):
        return 0 <= x < self.my_size and 0 <= y < self.my_size

    def get_field(self):
        return self.field

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
