class AIPlayer:
    def __init__(self, moveFunc, evaluate_func, statistics_func, type, param):
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        self.statistics_func = statistics_func
        self.type = type
        self.param = param
        
    def move(self, state):
        temp = self.moveFunc(state, self.evaluateFunc, self.param)
        temp.update_initial_moves()
        return temp
    
    def show_statistics(self, screen, font):
        if (self.statistics_func):
            self.statistics_func(screen, font)
