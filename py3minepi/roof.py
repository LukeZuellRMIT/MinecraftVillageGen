from mcpi import minecraft
import mcpi.block as block


def generateRoof(houseLength, houseWidth, wallHeight, x, y, z, buildBlock, roofType, roofHeight):
    mc = minecraft.Minecraft.create()
    
    # Sets initial layer
    mc.setBlocks(x + houseWidth - 1, y + wallHeight, z + houseLength - 1, x - houseWidth + 1, y + wallHeight, z - houseLength + 1, buildBlock)
    
    if roofType == 1:
        # Slab roof
        mc.setBlocks(x + houseWidth + 1, y + wallHeight + 1, z + houseLength + 1, x - houseWidth - 1, y + wallHeight + 1, z - houseLength - 1, 44, 2)
        mc.setBlocks(x + houseWidth - 1, y + wallHeight + 1, z + houseLength - 1, x - houseWidth + 1, y + wallHeight + 1, z - houseLength + 1, 5)
        mc.setBlocks(x + houseWidth - 3, y + wallHeight + 2, z + houseLength - 3, x - houseWidth + 3, y + wallHeight + 2, z - houseLength + 3, 44, 2)
        
    elif roofType == 2:
        
        for i in range(roofHeight):  
            # Makes slanted part of roof
            mc.setBlocks(x - houseWidth - 1 + i, y + wallHeight + 1 + i, z - houseLength - 1, x - houseWidth - 1 + i, y + wallHeight + 1 + i, z + houseLength + 1, 109, 8)

        for i in range(roofHeight):  
            # Makes slanted part of roof
            mc.setBlocks(x + houseWidth + 1 - i, y + wallHeight + 1 + i, z - houseLength - 1, x + houseWidth + 1 - i, y + wallHeight + 1 + i, z + houseLength + 1, 109, 1)
            
        for i in range(roofHeight - 1):  
            # fills planks in roof
            mc.setBlocks(x + houseWidth - i, y + wallHeight + 1 + i, z - houseLength + 1, x - houseWidth + i, y + wallHeight + 1 + i, z - houseLength + 1, 98)
            mc.setBlocks(x + houseWidth - i, y + wallHeight + 1 + i, z + houseLength - 1, x - houseWidth + i, y + wallHeight + 1 + i, z + houseLength - 1, 98)
            
            if 0 < i and i < roofHeight -2:
                # Windows in roof
                mc.setBlocks(x + houseWidth - i - 1, y + wallHeight + 1 + i, z - houseLength + 1, x - houseWidth + i + 1, y + wallHeight + 1 + i, z - houseLength + 1, 20)
                mc.setBlocks(x + houseWidth - i - 1, y + wallHeight + 1 + i, z + houseLength - 1, x - houseWidth + i + 1, y + wallHeight + 1 + i, z + houseLength - 1, 20)
            
        
        # Top layer of roof
        mc.setBlocks(x + houseWidth - (roofHeight - 1), y + wallHeight + roofHeight, z + houseLength + 1, x - houseWidth + (roofHeight - 1), y + wallHeight + roofHeight, z - houseLength - 1, 98)
        
    elif roofType == 3:
        for i in range(roofHeight):  
            
            # North part of wall
            mc.setBlocks(x + houseWidth + 1 - i, y + wallHeight + 1 + i, z - houseLength - 1 + i, x - houseWidth - 1 + i, y + wallHeight + 1 + i, z - houseLength - 1 + i, 109, 2)
            
            # West part of roof
            mc.setBlocks(x - houseWidth - 1 + i, y + wallHeight + 1 + i, z - houseLength - 1 + i, x - houseWidth - 1 + i, y + wallHeight + 1 + i, z + houseLength + 1 - i, 109, 8)
            
            # East part of roof
            mc.setBlocks(x + houseWidth + 1 - i, y + wallHeight + 1 + i, z - houseLength - 1 + i, x + houseWidth + 1 - i, y + wallHeight + 1 + i, z + houseLength + 1 - i, 109, 1)
            
            # South part of wall
            mc.setBlocks(x - houseWidth - 1 + i, y + wallHeight + 1 + i, z + houseLength + 1 - i, x + houseWidth + 1 - i, y + wallHeight + 1 + i, z + houseLength + 1 - i, 109, 3)
            
        mc.setBlocks(x + houseWidth - (roofHeight - 1), y + wallHeight + roofHeight, z + houseLength - (roofHeight - 1), x - houseWidth + (roofHeight - 1), y + wallHeight + roofHeight, z - houseLength + (roofHeight - 1), 98)
            
        for i in range(roofHeight):
            # Fixes misaligned stairs from south and east facing walls. Not sure why I need to place air block first but this is the only way it works.
            mc.setBlock(x + houseWidth - i, y + wallHeight + 1 + i, z + houseLength + 1 - i, 0)
            mc.setBlock(x + houseWidth - i, y + wallHeight + 1 + i, z + houseLength + 1 - i, 109, 3)
           
            
            
            
            
            
            