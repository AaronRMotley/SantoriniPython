import Worker as w

class Player: 
    def __init__(self, color, god = ''):
        self.workers = []
        self.god = god
        self.color = color

    def add_worker(self):
        self.workers.append(w.Worker())
