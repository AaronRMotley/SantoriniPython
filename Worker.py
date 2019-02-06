
import CellState

win, nowin = 1, 0

class Worker:
    def __init__(self, id, player, row, column):
          self.player = player
          #Worker ID = 0 is null. ID >1 is real
          self.id = id
          self.moved = False
          self.ascended = False
          self.level = 0

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
