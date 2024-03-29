import numpy as np
import random
import time
import pygame
from memory_profiling import *

simulations = 0
explored = 0

class Node:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.playouts = 0
        self.wins = 0
        self.parent = None
        self.generator = self.state.get_all_moves()
        self.fully_expanded = False
        self.unused = list(self.generator)

    """def expand(self):
        child = next(self.generator, None)
        if (child):
            new_node = Node(child)
            new_node.parent = self
            new_node.state.player = not new_node.state.player
            self.children.append(new_node)
            return new_node
        else:
            self.fully_expanded = True"""
    
    def expand(self):
        global explored
        if len(self.unused) == 0:
            self.fully_expanded = True
            return None
        i = random.randrange(len(self.unused)) 
        self.unused[i], self.unused[-1] = self.unused[-1], self.unused[i]    
        move = self.unused.pop()  
        new_node = Node(move)
        new_node.parent = self
        new_node.state.player = not new_node.state.player
        self.children.append(new_node)
        explored += 1
        return new_node

    def addChild(self, child):
        self.children.append(child)

    def best_child(self, c_param=0.1):
        choices_weights = [(c.wins / c.playouts) + c_param * np.sqrt((2 * np.log(self.playouts) / c.playouts)) for c in self.children]
        return self.children[np.argmax(choices_weights)]



def traverse(node):
    curr = node
    while curr.state.winner == 2:
        if not curr.fully_expanded:
            test = curr.expand()
            if (test):
                return test
            else:
                curr = curr.best_child()
        else:
            curr = curr.best_child()
    return curr

def rollout(node):
    global simulations
    curr = node.state
    while curr.winner == 2:
        moves = list(curr.get_all_moves())
        selected = random.choice(moves)
        curr = selected

    simulations += 1
    return curr.winner

def backpropagate(leaf, simulation_result, player):
    leaf.playouts += 1
    if simulation_result == player:
        leaf.wins += 1
    if (leaf.parent):
        backpropagate(leaf.parent, simulation_result, player)


def monte_carlo_tree_search(root, time_limit):
    startT = time.time()
    while (time.time() - startT < time_limit):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result, root.state.player)

    return root.best_child()

def show_mcts_statistics(screen, font):
    display_text = font.render(f"{explored} explored, {simulations} playouts", True, (0,0,0))
    textRect = display_text.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(display_text, textRect)
    pygame.display.flip()

@profile
def execute_mcts_move(state, _):
    return monte_carlo_tree_search(Node(state), 5).state