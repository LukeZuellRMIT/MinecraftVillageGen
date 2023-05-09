from time import sleep
from mcpi import minecraft
from mcrcon import MCRcon

mcr = MCRcon("localhost", "123")
mcr.connect()

def createPillars(houseLength, houseWidth, wallHeight, x, y, z, num):
    
    mc = minecraft.Minecraft.create()


    #west row
    mc.setBlocks(x - houseWidth, y + wallHeight, z - houseLength + 1, x - houseWidth, y + wallHeight, z + houseLength - 1, 109, 4)
    #north row
    mc.setBlocks(x - houseWidth + 1, y + wallHeight, z - houseLength, x + houseWidth - 1, y + wallHeight, z - houseLength, 109, 6)
    #east row
    mc.setBlocks(x + houseWidth, y + wallHeight, z + houseLength - 1, x + houseWidth, y + wallHeight, z - houseLength + 1, 109, 5)
    #south row
    mc.setBlocks(x + houseWidth - 1, y + wallHeight, z + houseLength, x - houseWidth + 1, y + wallHeight, z + houseLength, 109, 7)


    #TOP/BOTTOM CORNER BLOCKS
    
    #north-west
    mc.setBlock(x - houseWidth, y + wallHeight, z - houseLength, 98)
    mc.setBlock(x - houseWidth, y, z - houseLength, 98)
    #north-east
    mc.setBlock(x + houseWidth, y + wallHeight, z - houseLength, 98)
    mc.setBlock(x + houseWidth, y, z - houseLength, 98)
    #south-west
    mc.setBlock(x - houseWidth, y + wallHeight, z + houseLength, 98)
    mc.setBlock(x - houseWidth, y, z + houseLength, 98)
    #south-east
    mc.setBlock(x + houseWidth, y + wallHeight, z + houseLength, 98)
    mc.setBlock(x + houseWidth, y, z + houseLength, 98)


    #PILLARS
   

    #LEAF BOTTOM LINING
    mc.setBlocks(x - houseWidth, y + 1, z - houseLength, x - houseWidth, y + wallHeight - 1, z - houseLength, 17)
    mc.setBlocks(x + houseWidth, y + 1, z - houseLength, x + houseWidth, y + wallHeight - 1, z - houseLength, 17)
    mc.setBlocks(x - houseWidth, y + 1, z + houseLength, x - houseWidth, y + wallHeight - 1, z + houseLength, 17)
    mc.setBlocks(x + houseWidth, y + 1, z + houseLength, x + houseWidth, y + wallHeight - 1, z + houseLength, 17)
