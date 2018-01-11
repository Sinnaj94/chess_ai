import numpy as np
import math

class Game_Manager():
    def __init__(self):
        self.board = Board()
        self.player1 = Player("Me", False, self.board)
        self.player2 = Player("Bot", True, self.board)


class Board():
    def __init__(self):
        self.size = 8
        self.field = np.zeros((self.size, self.size))

    # see if the position is possible on the field or not
    def move_possible(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size


class Player():
    def __init__(self, name, inverted, board):
        self.name = name
        self.board = board
        # indicator, if player is on another site.
        self.inverted = inverted
        self.main_delta = 0
        if inverted:
            self.main_delta = self.board.size - 1

        self.distribute()

    def distribute(self):
        # pawns
        pawns = []
        for x in range(0, self.board.size):
            pawns.append(Pawn(math.fabs(self.main_delta - x), math.fabs(self.main_delta - 1)))
        for p in pawns:
            p.print_me()

    def move(self):
        raise NotImplementedException()


class Piece():
    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        if not character:
            self.character = "1"
        else:
            self.character = character

    def own_move_possibilities(self):
        return [0,0]

    def print_me(self):
        print self.character + " at " + str(self.x) + ", " + str(self.y)

class Pawn(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y, "P")

    # delta of move possibilities
    def own_move_possibilities(self):
        if self.y == 1:
            return [0,1],[0,2]
        return [0,1]

game_manager = Game_Manager()