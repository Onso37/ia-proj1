import numpy

def heuristic1(player, state):
    count_a = numpy.count_nonzero(state.board == player)
    count_b = numpy.count_nonzero(state.board == (not player))
    return count_a - count_b
