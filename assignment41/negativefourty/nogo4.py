#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

#!/usr/bin/python3
# Set the path to your python3 above



from gtp_connection import GtpConnection, point_to_coord, format_point
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR, BLACK, WHITE, EMPTY, BORDER
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine
from ucb import ucb_run
import numpy as np
import random
from math import log,sqrt
import sys



class NoGo:
    def __init__(self):
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        GoEngine.__init__(self, "NoGo4", 1.0)
        self.noOfSim = 30

    def random_simulation(self, board,  move):
        board_copy = board.copy()
        current = board.current_player
        board_copy.play_move(move, current)
        while True:
            current = board_copy.current_player
            move = self.random_move(board_copy, current)
            if move == None:
                return BLACK+WHITE-current
            board_copy.play_move(move,current)    

    def random_move(self, board, player):
            moves = board.get_empty_points()
            np.random.shuffle(moves)
            for move in moves:
                legal = board.is_legal(move, player)
                if legal:
                    return move
            return None


    def generate_legal(self, gameState, color):
        points = gameState.get_empty_points()
        moves = []
        for pt in points:
            if gameState.is_legal(pt, color):
                moves.append(pt)
        return moves

    def simulate(self, board, move):
        return self.random_simulation(board, move)
                

    def get_move(self, board, color):
        board_copy = board.copy()
        moves = self.generate_legal(board_copy,color)
        if not moves:
            return None
        elif len(moves) == 1:
            return moves[0]
        else:
            move = ucb_run(self, board_copy, 0.4, moves, color)
            return move
        
    


def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(NoGo(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
