class AIPlayer:
    def __init__(self, moveFunc, evaluate_func, statistics_func, type):
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        self.statistics_func = statistics_func
        self.type = type
        
    def move(self, state):
        temp = self.moveFunc(state, self.evaluateFunc)
        temp.update_initial_moves()
        temp.moved_pos = []
        return temp
    
    def show_statistics(self, screen, font):
        if (self.statistics_func):
            self.statistics_func(screen, font)
