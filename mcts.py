import numpy as np
import random
import time
import pygame
from memory_profiler import profile

simulations = 0
explored = 0
wins=0

class Node:
    """Node class used in MCTS."""

    def __init__(self, state):
        """Creates a new mode from a given state and initializes its list of unused moves."""
        self.state = state
        self.children = []
        self.playouts = 0
        self.wins = 0
        self.parent = None
        self.generator = self.state.get_all_moves()
        self.fully_expanded = False
        self.unused = list(self.generator)
    
    def expand(self):
        """Removes a random move from the unused list and returns it. If it is empty, fully_expanded is set to True on the Node object."""
        global explored
        if len(self.unused) == 0:
            self.fully_expanded = True
            return None
        i = random.randrange(len(self.unused)) 
        self.unused[i], self.unused[-1] = self.unused[-1], self.unused[i]    
        move = self.unused.pop()  
        new_node = Node(move)
        new_node.parent = self
        new_node.state.player = 1 -  new_node.state.player
        self.children.append(new_node)
        explored += 1
        return new_node

    def addChild(self, child):
        """Adds a child node to the object."""
        self.children.append(child)

    def best_child(self, c_param=0.1):
        """Returns the best child of the node according to the UCT formula."""
        choices_weights = [(c.wins / c.playouts) + c_param * np.sqrt((np.log(self.playouts) / c.playouts)) for c in self.children]
        return self.children[np.argmax(choices_weights)]



def traverse(node):
    """"Traverses the best children of the tree until a leaf is found. When a leaf node is found, it is expanded and the resulting child is selected."""
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
    """Performs a playout from a given node, picking random moves until a terminal node is reached."""
    global simulations
    curr = node.state
    while curr.winner == 2:
        moves = list(curr.get_all_moves())
        selected = random.choice(moves)
        curr = selected

    simulations += 1
    return curr.winner

def backpropagate(leaf, simulation_result, player):
    """Propagates the simulation result back to the root. The "player" argument is the player who is playing at the root."""
    global wins
    leaf.playouts += 1
    if simulation_result == player:
        wins += 1
        leaf.wins += 1
    if (leaf.parent):
        backpropagate(leaf.parent, simulation_result, player)


def monte_carlo_tree_search(root, time_limit):
    """Uses the MCTS algorithm to find a move, running simulations until the time limit is reached."""
    player = root.state.player
    startT = time.time()
    while (time.time() - startT < time_limit):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result, player)

    return root.best_child()

def show_mcts_statistics(screen, font, first):
    """Shows the statistics from the last MCTS execution: number of wins and number of total simulations."""
    text = f"{wins} win, {simulations} playouts"
    if first:
        print(text)
    display_text = font.render(text, True, (0,0,0))
    textRect = display_text.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(display_text, textRect)
    pygame.display.flip()
   
def execute_mcts_move(state, _, seconds,__,___):
    """Executes a MCTS move from a given state. After 'seconds' seconds, the algorithm will stop creating new simulations."""
    global simulations, wins
    simulations = 0
    wins = 0
    return monte_carlo_tree_search(Node(state), seconds).state