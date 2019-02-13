
win, nowin = 1, 0

class Worker:
    def __init__(self):
        self.player = 0
        self.id = 0
        self.color = ''
        self.moved = False
        self.ascended = False
        self.level = 0
    
    def assignPlayer(self, player, id):
        self.player = player
        self.id = id
        if player == 1:
            self.color = "R"
        elif player == 2:
            self.color = "B"
        else:
            self.color = "G"
        
    def move(self, newlevel):
        self.moved = True
        if newlevel-self.level == 1:
            self.ascended = True
            self.level = newlevel
            if self.level == 3:
                return win
        elif newlevel-self.level == -1:
            self.level = newlevel
            self.ascended = False
        elif newlevel - self.level == 0:
            self.ascended = False
        elif newlevel - self.level == -2:
            #Win as a god
            pass
        else:
            #Error
            pass
        return nowin

        