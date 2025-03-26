class AIPlayer:
    """Class used to represent AI players and execute their moves through a common interface"""
    
    def __init__(self, moveFunc, evaluate_func, statistics_func, type, param, prune_shorts, ab_cut):
        """Constructor of AIPlayer. Takes a function to execute a move, one to evaluate states (only needed for Minimax), one to show statistics (can be null),
        a numeric parameter (depth for Minimax, max seconds for MCTS), and whether or not to prune short moves on Minimax"""
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        self.statistics_func = statistics_func
        self.type = type
        self.param = param
        self.prune_shorts = prune_shorts
        self.ab_cut = ab_cut
        
    def move(self, state):
        """Calls the move function to execute a move from a given state and return its corresponding state."""
        if self.prune_shorts == 2:
            temp = self.moveFunc(state, self.evaluateFunc, self.param, True, self.ab_cut)
        else:
            temp = self.moveFunc(state, self.evaluateFunc, self.param, False, self.ab_cut)
        temp.update_initial_moves()
        return temp
    
    def show_statistics(self, screen, font, first):
        """Displays the statistics on the screen, if there are any."""
        if (self.statistics_func):
            self.statistics_func(screen, font, first)
