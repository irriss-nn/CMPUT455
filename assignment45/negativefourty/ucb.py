import numpy as np
import random
from math import log,sqrt

INFINITY = float('inf')

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
        result = self.simulate(board, moves[moveIndex])
        if result == toplay:
            stats[moveIndex][0] += 1
        stats[moveIndex][1] += 1
    bestIndex = bestArm(stats)
    best = moves[bestIndex]
    return best