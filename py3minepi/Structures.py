
# Structures class lays a framework for each type of structure:
#   - Well
#   - Garden
#   - Playground
class Structures():
    
    def __init__ (self, x, y, z, length, width, structure_type):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.structure_type = structure_type
        
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getZ(self):
        return self.z
    
    def setY(self, y):
        self.y = y
    
    def getType(self):
        return self.structure_type
    
    def getLength(self):
        return self.length

    def getWidth(self):
        return self.width