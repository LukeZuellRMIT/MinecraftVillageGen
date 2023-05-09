from mcpi import minecraft

class Grid():
    
    def __init__(self, x, z):
        self.gridPositions = []
        self.x = x
        self.z = z
        
    
    # Generates a 4 x 4 grid of 20 x 20 block pieces of land. 
    # The central positions are used as co-ordinates for places houses.
    def generateGrid(self):
        # grid is 80 x 80 and the first edge is at (x - 40, z - 40)
        # Start position is (x - 30, z - 30)
        # each grid sections is 20 x 20 blocks.

        positions = []
        initial_x = self.x
        initial_z = self.z

        for x_vals in range(4):
            current_x = initial_x - 30 + x_vals * 20
            
            for z_vals in range(4):
                current_z = initial_z - 30 + z_vals * 20
                
                positions.append([current_x, current_z])
        
        self.gridPositions = positions
    
    # Show grid is used for debugging purposes. It places a pillar of glass
    # at the centre position of the block of land.
    def showGrid(self):
        mc = minecraft.Minecraft.create()
        
        initial_x = self.x
        initial_z = self.z
        
        for x_vals in range(4):
            current_x = initial_x - 30 + x_vals * 20
            
            for z_vals in range(4):
                current_z = initial_z - 30 + z_vals * 20
                height = mc.getHeight(current_x, current_z)
                
                mc.setBlocks(current_x, height, current_z, current_x, height + 25, current_z, 20)
