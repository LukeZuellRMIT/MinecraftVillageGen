from mcpi import minecraft

def windowLayer(houseWidth, houseLength, x, z, y, orientation, buildBlock):
    mc = minecraft.Minecraft.create()
    
    # Places window blocks 
    if orientation != 'width':
        mc.setBlocks(x + houseWidth + 1, y, z - houseLength, x + houseWidth + 1, y, z + houseLength, 102) # sets glass
        mc.setBlock(x + houseWidth + 1, y, z - houseLength - 1, 0) # fixes corners
        mc.setBlock(x + houseWidth + 1, y, z - houseLength - 1, buildBlock) # fixes corners
        mc.setBlock(x + houseWidth + 1, y, z + houseLength + 1, 0) # fixes corners
        mc.setBlock(x + houseWidth + 1, y, z + houseLength + 1, buildBlock) # fixes corners
        mc.setBlocks(x + houseWidth, y, z - houseLength, x + houseWidth, y, z + houseLength, 1) # fixes rest - spawns stone
        mc.setBlocks(x + houseWidth, y, z - houseLength, x + houseWidth, y, z + houseLength, 0) # fixes rest - removes stone

        mc.setBlocks(x - houseWidth - 1, y, z - houseLength, x - houseWidth - 1, y, z + houseLength, 102)
        mc.setBlock(x - houseWidth - 1, y, z - houseLength - 1, 0) # fixes corners
        mc.setBlock(x - houseWidth - 1, y, z - houseLength - 1, buildBlock) # fixes corners
        mc.setBlock(x - houseWidth - 1, y, z + houseLength + 1, 0) # fixes corners
        mc.setBlock(x - houseWidth - 1, y, z + houseLength + 1, buildBlock) # fixes corners
        mc.setBlocks(x - houseWidth, y, z - houseLength, x + houseWidth, y, z + houseLength, 1)
        mc.setBlocks(x - houseWidth, y, z - houseLength, x + houseWidth, y, z + houseLength, 0)
        
    else:
        mc.setBlocks(x - houseWidth, y, z - houseLength - 1, x + houseWidth, y, z - houseLength - 1, 102)
        mc.setBlock(x - houseWidth, y, z + houseLength - 1, 0)
        mc.setBlock(x - houseWidth, y, z + houseLength - 1, buildBlock)
        mc.setBlock(x - houseWidth, y, z - houseLength + 1, 0)
        mc.setBlock(x - houseWidth, y, z - houseLength + 1, buildBlock)
        mc.setBlocks(x - houseWidth, y, z - houseLength, x + houseWidth, y, z - houseLength, 1)
        mc.setBlocks(x - houseWidth, y, z - houseLength, x + houseWidth, y, z - houseLength, 0)

        mc.setBlocks(x - houseWidth, y, z + houseLength + 1, x + houseWidth, y, z + houseLength + 1, 102)
        mc.setBlock(x - houseWidth, y, z + houseLength - 1, 0)
        mc.setBlock(x - houseWidth, y, z + houseLength - 1, buildBlock)
        mc.setBlock(x - houseWidth, y, z - houseLength + 1, 0)
        mc.setBlock(x - houseWidth, y, z - houseLength + 1, buildBlock)
        mc.setBlocks(x - houseWidth, y, z + houseLength, x + houseWidth, y, z + houseLength, 1)
        mc.setBlocks(x - houseWidth, y, z + houseLength, x + houseWidth, y, z + houseLength, 0)
        
    
    return


def generateWindows(height, houseLength, houseWidth, x, z, y, buildBlock):
    
    if height > 4:
        windowLayer(houseWidth, houseLength, x, z, y + 1, 'width', buildBlock)
        windowLayer(houseWidth, houseLength, x, z, y + 2, 'width', buildBlock)
    else:
        windowLayer(houseWidth, houseLength, x, z, y + 1, 'width', buildBlock)
    
    if height > 4:
        windowLayer(houseWidth, houseLength, x, z, y + 1, 'length', buildBlock)
        windowLayer(houseWidth, houseLength, x, z, y + 2, 'length', buildBlock)
    else:
        windowLayer(houseWidth, houseLength, x, z, y + 1, 'length', buildBlock)
    
    return


