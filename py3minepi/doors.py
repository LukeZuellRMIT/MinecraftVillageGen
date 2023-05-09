from mcpi import minecraft
import random

def generateDoor(houseLength, houseWidth, x, y, z, buildBlock):
    mc = minecraft.Minecraft.create()
    
    # front of house
    doorFacing = ''
    doorSide = random.randint(1, 4) # choosing a side to go on
    if doorSide == 1 or doorSide == 3: #if 'north' or 'south' then get .. width..? 
        doorPosition = random.randint(-houseWidth + 5, houseWidth - 5) # chooses random available spot
        if doorSide == 1: # north
            doorFacing = 'N'
            mc.setBlocks(x + doorPosition - 1, y, z - houseLength + 1, x + doorPosition + 1, y + 2, z - houseLength + 1, buildBlock) # around door
            mc.setBlock(x + doorPosition, y + 1, z - houseLength + 1, 64, 10) # top
            mc.setBlock(x + doorPosition, y, z - houseLength + 1, 64, 1) # bottom
            mc.setBlock(x + doorPosition, y, z - houseLength, 0) # remove leaf
            doorCoords = x + doorPosition, y, z - houseLength + 1 # coords for bottom half door to return

        else: # south
            doorFacing = 'S'
            mc.setBlocks(x - doorPosition + 1, y, z + houseLength - 1, x - doorPosition - 1, y + 2, z + houseLength - 1, buildBlock) # around door
            mc.setBlock(x - doorPosition, y + 1, z + houseLength - 1, 64, 12) # top
            mc.setBlock(x - doorPosition, y, z + houseLength - 1, 64, 3) # bottom
            mc.setBlock(x - doorPosition, y, z + houseLength, 0) # remove leaf
            doorCoords = x - doorPosition, y, z + houseLength - 1 # coords for bottom half door to return      
            
    # getting if east or west sided
    else:
        doorPosition = random.randint(-houseLength + 3, houseLength - 3) # chooses random available spot
        if doorSide == 2: # west
            doorFacing = 'W'
            mc.setBlocks(x - houseWidth + 1, y, z + doorPosition - 1, x - houseWidth + 1, y + 2, z + doorPosition + 1, buildBlock) # around door
            mc.setBlock(x - houseWidth + 1, y + 1, z + doorPosition, 64, 9) # top
            mc.setBlock(x - houseWidth + 1, y, z + doorPosition, 64, 0) # bottom
            mc.setBlock(x - houseWidth, y, z + doorPosition, 0) # remove leaf
            doorCoords = x - houseWidth + 1, y, z + doorPosition # coords for bottom half door to return

        else: # east
            doorFacing = 'E'
            mc.setBlocks(x + houseWidth - 1, y, z - doorPosition + 1, x + houseWidth - 1, y + 2, z - doorPosition - 1, buildBlock) # around door
            mc.setBlock(x + houseWidth - 1, y + 1, z - doorPosition, 64, 11) # top
            mc.setBlock(x + houseWidth - 1, y, z - doorPosition, 64, 2) # bottom
            mc.setBlock(x + houseWidth, y, z - doorPosition, 0) # remove leaf
            doorCoords = x + houseWidth - 1, y, z - doorPosition # coords for bottom half door to return

    #print(doorCoords) 
    return [doorCoords, doorFacing]

    #print(houseWidth)
    #print(houseLength)
    #print(doorPosition)
    #mc.setBlocks(x + 2 - houseWidth - 1, y, z - 1, x + 2 - houseWidth - 1, y + 2, z + 1, 87) # around door
    #mc.setBlock(x + 2 - houseWidth - 1, y + 1, z, 64, 9) # top
    #mc.setBlock(x + 2- houseWidth - 1, y, z, 64, 0) # bottom
    #mc.setBlock(x + 1 - houseWidth - 1, y, z, 0) # air to remove leaf
    #return doorPosition
    #mc.setBlocks(x + 2 - houseWidth - 1, y, z + 1, x + 2 - houseWidth - 1, y + 2, z + 1, 87) # left
    #mc.setBlocks(x + 2 - houseWidth - 1, y, z - 1, x + 2 - houseWidth - 1, y + 2, z - 1, 88) # right
    #mc.setBlock(x + 2 - houseWidth - 1, y + 2, z, 89) # top
    # back of house
    #mc.setBlock(x + houseWidth - 1, y + 1, z, 64, 13) # top
    #mc.setBlock(x + houseWidth - 1, y, z, 64, 2) # bottom
    #mc.setBlock(x + 1 + houseWidth - 1, y, z, 0) # air to remove leaf
    
