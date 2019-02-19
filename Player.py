import Worker as wk

class Player: 
    def __init__(self, color, god = ''):
        self.workers = []
        self.god = god
        self.color = color