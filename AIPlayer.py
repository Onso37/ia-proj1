class AIPlayer:
    def __init__(self, moveFunc):
        self.moveFunc = moveFunc
        
    def move(self, state):
        return self.moveFunc(state)