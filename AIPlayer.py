class AIPlayer:
    def __init__(self, moveFunc, evaluate_func):
        self.moveFunc = moveFunc
        self.evaluateFunc = evaluate_func
        
    def move(self, state):
        return self.moveFunc(state, self.evaluateFunc)