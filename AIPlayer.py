class AIPlayer:
    def __init__(self, moveFunc, evaluate_func, statistics_func, type, param, prune_shorts,ab_cut):
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        self.statistics_func = statistics_func
        self.type = type
        self.param = param
        self.prune_shorts = prune_shorts
        self.ab_cut = ab_cut
        
    def move(self, state):
        if self.prune_shorts == 2:
            temp = self.moveFunc(state, self.evaluateFunc, self.param, True, self.ab_cut)
        else:
            temp = self.moveFunc(state, self.evaluateFunc, self.param, False, self.ab_cut)
        temp.update_initial_moves()
        return temp
    
    def show_statistics(self, screen, font, first):
        if (self.statistics_func):
            self.statistics_func(screen, font, first)
