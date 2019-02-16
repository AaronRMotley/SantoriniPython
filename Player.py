import Worker as w

class Player: 
    def __init__(self, god):
        self.workers = []

    def addworker(self):
        self.workers.append(w.Worker())