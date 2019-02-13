import Worker

class Cell:
    def __init__(self, perimeter = False):
        self.level = 0
        self.occupied = False
        self.dome = False
        self.perimeter = perimeter
        self.workerid = 0
        
    
    def build(self):
        if self.level < 4:
            self.level += 1
        if self.level >= 4:
            self.dome = True

    def destroy(self):
        if self.level > 0 and self.dome != True:
            self.level -= 1
    
    def getvariablestoprint(self):
        return ["level", self.level, "occupied", self.occupied, "dome", self.dome, "perimeter", self.perimeter, "workerid", self.workerid]
    
    def getvariables(self):
        return [self.level, self.occupied, self.dome, self.perimeter, self.workerid]
