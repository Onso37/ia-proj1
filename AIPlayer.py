class AIPlayer:
    def __init__(self, moveFunc, evaluate_func, type):
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        self.type = type
        
    def move(self, state):
        return self.moveFunc(state, self.evaluateFunc)