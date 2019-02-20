NULL = ''

class Player:
    def __init__(self, color, god=NULL):
        self.workers = [Worker(color, 1), Worker(color, 2)]
        self.god = god


class Worker:
    def __init__(self, color, id):
        self.moved = False
        self.ascended = False
        self.color = color
        self.id = id

    def move(self, old_level, new_level):
        self.moved = True
        if new_level-old_level == 1:
            self.ascended = True
            old_level = new_level
            if old_level == 3:
                pass
                # Win Condition
        elif new_level-old_level == -1:
            old_level = new_level
            self.ascended = False
        elif new_level - old_level == 0:
            self.ascended = False
        elif new_level - old_level == -2:
            # Win as a Satyr God
            pass
        else:
            # Error
            pass
