from mcpi import minecraft
from mcrcon import MCRcon
import random

# Import all required files
import windows as windowFile
import doors as doorFile
import pillars as pillarFile
import walls as wallFile
import utils as generateUtil

import roof as roofFile

mcr = MCRcon("localhost", "123")
mcr.connect()


class House():
    
    # Initialises the required values for a house.
    def __init__(self, x, y, z, length, width, height, roofStyle, floors):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.height = height
        self.roofStyle = roofStyle
        self.doorPosition = ()
        self.doorFacing = ''
        self.floors = floors
        self.innerWallPos = []
        
    def getx(self):
        return self.x
    
    def gety(self):
        return self.y
        
    def getz(self):
        return self.z
    
    def sety(self, y):
        self.y = y
        
    def getWidth(self):
        return self.width
        
    def getLength(self):
        return self.length
        
    # Calling this function builds a house.
    def generateHouse(self):
        mc = minecraft.Minecraft.create()
        
        x = self.x
        y = self.y 
        z = self.z 
        houseLength = self.length
        houseWidth = self.width
        houseHeight = self.height
        roofStyle = self.roofStyle
        floors = self.floors
        
        # making a specific block list, will allow for list of lists later to choose house 'theme' 
        blockList = [98, 5]
        buildBlock = random.choice(blockList)

        if buildBlock == 45: # if brick, brick stair
            stairBlock = 108 
        elif buildBlock == 5: # wooden stair
            stairBlock = 53
        else: # else stone brick
            stairBlock = 109

        wallHeight = houseHeight - 1
        
        # passing values into specific files/functions
        # creates air for clear space for the house
        mc.setBlocks(x - houseWidth, y - 1, z - houseLength, x + houseWidth, y + houseHeight, z + houseLength, 0, buildBlock)

        # outside walls (bc they sink into the ground i think)
        if floors > 2:
            wallFile.createWalls(houseLength, houseWidth, wallHeight * floors + floors + (floors - 2), x, y, z, buildBlock)
        else:
            wallFile.createWalls(houseLength, houseWidth, wallHeight * floors + floors + floors, x, y, z, buildBlock)
        
        # rest checkers
        if floors > 1:
            # roofs n pillars as only need one
            pillarFile.createPillars(houseLength, houseWidth, wallHeight * floors + floors + (floors - 1), x, y, z, buildBlock)
            roofFile.generateRoof(houseLength, houseWidth, wallHeight * floors + floors + (floors - 1), x, y, z, buildBlock, roofStyle, 4)
            # per level stuff (floor n windows)
            for i in range(1, floors + 1):
                windowFile.generateWindows(houseHeight, houseLength  - 2, houseWidth - 2, x, z, y + (4 * (i - 1)), buildBlock)
                mc.setBlocks(x - houseWidth + 1, y - 1 + (4 * (i - 1)), z - houseLength + 1, x + houseWidth - 1, y - 1 + (4 * (i - 1)), z + houseLength - 1, 1, buildBlock) 
        else:
            pillarFile.createPillars(houseLength, houseWidth, wallHeight * floors + floors, x, y, z, buildBlock)
            roofFile.generateRoof(houseLength, houseWidth, wallHeight * floors + floors, x, y, z, buildBlock, roofStyle, 4)

        # bottom window           
        windowFile.generateWindows(houseHeight, houseLength  - 2, houseWidth - 2, x, z, y, buildBlock)

        # bottom floor 
        mc.setBlocks(x - houseWidth, y - 1, z - houseLength, x + houseWidth, y - 1, z + houseLength, 98) # stone brick

        # door pos
        doorData = doorFile.generateDoor(houseLength, houseWidth, x, y, z, buildBlock)
        self.doorPosition = doorData[0]
        self.doorFacing = doorData[1]
        
        # Places the inner walls of the house.
        for i in range(0, floors):
            if houseLength > houseWidth:
                self.innerWallPos += wallFile.createInnerWalls(houseLength*2 - 2, houseWidth*2 - 2, wallHeight, x + houseWidth - 1, y + ((wallHeight+2)*i), z - houseLength + 1, buildBlock,'W', 0, self.doorPosition, self.doorPosition)
                mc.setBlocks(x - houseWidth + 1, y + (wallHeight * (i + 1)) + 1, z - houseLength + 1, x + houseWidth - 1, y + (wallHeight * (i + 1)) + 1, z + houseLength - 1, buildBlock)
            else:
                self.innerWallPos += wallFile.createInnerWalls(houseLength*2 - 2, houseWidth*2 - 2, wallHeight, x + houseWidth - 1, y + ((wallHeight+2)*i), z - houseLength + 1, buildBlock,'S', 0, self.doorPosition, self.doorPosition)
                mc.setBlocks(x - houseWidth + 1, y + (wallHeight * (i + 1)) + 1, z - houseLength + 1, x + houseWidth - 1, y + (wallHeight * (i + 1)) + 1, z + houseLength - 1, buildBlock)
        
        # Places the stair case connection the different levels of the house.
        generateUtil.generateStairs(houseLength, houseWidth, x, y, z, floors, stairBlock)