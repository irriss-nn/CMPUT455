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
import numpy as np
import random
from math import log,sqrt
import sys

INFINITY = float('inf')
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
        self.noOfSim = 50


    
    
    # def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
    #     return GoBoardUtil.generate_random_move(board, color,
    #                                             use_eye_filter=False)

    def randomMove(self, state, player):
            moves = state.get_empty_points()
            np.random.shuffle(moves)
            for move in moves:
                legal = state.is_legal(move, player)
                if legal:
                    return move
            return None

    def evaluate(self, cp):
            return BLACK + WHITE - cp



    def randomSimulation(self, state,  move, play):
        state_copy = state.copy()
        state_copy.play_move(move, play)
        while True:
            current = state_copy.current_player
            move = self.randomMove(state_copy, current)
            if move == None:
                return self.evaluate(current)
            state_copy.play_move(move,current)


    def generateLegalMoves(self, gameState, color):
        ePts = gameState.get_empty_points()
        moves = []
        for pt in ePts:
            if gameState.is_legal(pt, color):
                moves.append(pt)
        return moves

    def simulate(self, state, move, toplay):
        return self.randomSimulation(state, move, toplay)
                
    def simulateMove(self, state, move, toplay):
        wins = 0 
        for _ in range(self.noOfSim):
            result = self.simulate(state, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def get_move(self, state, color):
        state_copy = state.copy()
        legalMoves = self.generateLegalMoves(state_copy,color)
        probability = {}
        if not legalMoves:
            return None
        elif len(legalMoves) == 1:
            return legalMoves[0]
        else:
            C = 0.4
            best =ucb_run(self, state_copy, C, legalMoves, color)
            return best

        





#...............................ucb.......................................................

    
def ucb(stats, C, i, n):
    if stats[i][1] == 0:
        return INFINITY
    mean = stats[i][0] / stats[i][1]
    return mean  + C * sqrt(log(n) / stats[i][1])

def findBest(stats, C, n):
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        score = ucb(stats, C, i, n) 
        if score > bestScore:
            bestScore = score
            best = i
    assert best != -1
    return best

def bestArm(stats):
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        if stats[i][1] > bestScore:
            bestScore = stats[i][1]
            best = i
    assert best != -1
    return best


def ucb_run(self, board, C, moves, toplay):
    stats = [[0,0] for i in moves]
    num_simulation = len(moves) * self.noOfSim
    for n in range(num_simulation):
        moveIndex = findBest(stats, C, n)
        result = self.simulate(board, moves[moveIndex], toplay)
        if result == toplay:
            stats[moveIndex][0] += 1
        stats[moveIndex][1] += 1
    bestIndex = bestArm(stats)
    best = moves[bestIndex]
    return best


def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(NoGo(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
