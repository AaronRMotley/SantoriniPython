
class Worker:
    def __init__(self):
        self.moved = False
        self.ascended = False
        
    def move(self, old_level, new_level):
        self.moved = True
        if new_level-old_level == 1:
            self.ascended = True
            old_level = new_level
            if old_level == 3:
                pass
                #Win Condition
        elif new_level-old_level == -1:
            old_level = new_level
            self.ascended = False
        elif new_level - old_level == 0:
            self.ascended = False
        elif new_level - old_level == -2:
            #Win as a Satyr God
            pass
        else:
            #Error
            pass

        