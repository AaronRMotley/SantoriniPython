import Worker as wk

class Cell:
    def __init__(self, perimeter = False):
        self.level = 0
        self.occupied = False
        self.dome = False
        self.perimeter = perimeter
        
    def build(self):
        if self.level < 4:
            self.level += 1
        if self.level >= 4:
            self.dome = True

    def destroy(self):
        if self.level > 0 and self.dome != True:
            self.level -= 1
    
    def print_pretty(self):
        return ["level", self.level, "occupied", self.occupied, "dome", self.dome, "perimeter", self.perimeter]
    
    def print_simple(self):
        return [self.level, self.occupied, self.dome, self.perimeter]
