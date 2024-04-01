class AIPlayer:
    def __init__(self, moveFunc, evaluate_func, statistics_func, type, param, prune_shorts):
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        self.statistics_func = statistics_func
        self.type = type
        self.param = param
        self.prune_shorts = prune_shorts
        
    def move(self, state):
        if self.prune_shorts == 2:
            temp = self.moveFunc(state, self.evaluateFunc, self.param, True)
        else:
            temp = self.moveFunc(state, self.evaluateFunc, self.param)
        temp.update_initial_moves()
        return temp
    
    def show_statistics(self, screen, font, first):
        if (self.statistics_func):
            self.statistics_func(screen, font, first)
