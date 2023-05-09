from audioop import reverse
from cmath import e
from copyreg import constructor
from re import X
from mcpi import minecraft
import time


# Allowing for minecraft server commands
# Server.properties file: enable-rcon - true, rcon.password - 123
# 'pip3 install mcrcon' in terminal/cmd
# use via MCRcon.command(f"*command*")
from mcrcon import MCRcon

# Importing math for specifc blocks coordinates
import math
import random

# Import all required files
import garden as gardenFile
import paths as pathFile
import terrains as terrainFile
import well as wellFile
import playground as playgroundFile
import grids as gridFile
import houses as houseFile
import scanning as scanning

# Initialise Minecraft insistance 
mc = minecraft.Minecraft.create()

# Setting up Rcon connection
mcr = MCRcon("localhost", "123")
mcr.connect()


# Terraform function is super slow right now, I plan on adding multi threading once the algorithm is complete. If you want to test houses just limit the number built to be 1.
# Currently the function just flattens land, ignores trees and filles in holes under the house. I am going to add smoothing tomorrow morning. ~ Mark 

class Village():
    
    # Initialises all the required values for a village.
    def __init__(self, numHouses, numExtras, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.houses = []
        self.extraStructures = []
        self.houseLocations = []
        self.extraLocations = []
        self.numHouses = numHouses
        self.numExtras = numExtras
        self.landBorders = []
        self.doorPositions = []
        
        
    # Gets the available positions for houses and extra structures.
    # Positions are then selected and removed from the available positions.
    def generatePositions(self):
        
        # Creates a grid for the houses to be placed in. The grid is 80 x 80 blocks
        # and contains 16 20 * 20 sections of land.
        grid_x = self.x
        grid_z = self.z
        newGrid = gridFile.Grid(grid_x, grid_z)
        newGrid.generateGrid()
        # To show the centre positions of each block of land un-comment below code. (Not meant to be active for full testing.)
        # newGrid.showGrid()
        
        locationOptions = newGrid.gridPositions
        selectedIndexs = []
        
        bad_blocks = [0, 175, 18, 161, 17, 162, 99, 100, 31]
        
        # Selects a piece of land for each house.
        for _ in range(self.numHouses):
            
            random_position  =  random.randint(0, 15)
            
            while random_position in selectedIndexs:
                random_position  =  random.randint(0, 15)
            
            x = locationOptions[random_position][0]
            z = locationOptions[random_position][1]
            
            block_height  = mc.getHeight(x, z)
            block_type = mc.getBlock(x, block_height, z)
            
            while block_type in bad_blocks:
                mc.setBlock(x, block_height, z, 0)
                block_height  = mc.getHeight(x, z)
                block_type = mc.getBlock(x, block_height, z)
            
            selectedIndexs.append(random_position)
          
            self.houseLocations.append({'xPos' : x, 'yPos': block_height, 'zPos': z})
            
        
        # Selects a peice of land for each structure.
        for _ in range(self.numExtras):
            
            random_position  =  random.randint(0, 15)
            
            while random_position in selectedIndexs:
                random_position  =  random.randint(0, 15)
            
            x = locationOptions[random_position][0]
            z = locationOptions[random_position][1]
            
            block_height  = mc.getHeight(x, z)
            block_type = mc.getBlock(x, block_height, z)
            
            while block_type in bad_blocks:
                mc.setBlock(x, block_height, z, 0)
                block_height  = mc.getHeight(x, z)
                block_type = mc.getBlock(x, block_height, z)
            
            selectedIndexs.append(random_position)
            self.extraLocations.append({'xPos' : x, 'yPos': block_height, 'zPos': z})
            
        
    # This populates the village with houses and extra structures.
    # It does not place them but generates their properties and stores them in the village.
    def generateVillage(self):
        
        # Adds houses to the village.
        for each in self.houseLocations:
            position = each
            x = math.floor(position['xPos'])
            y = math.floor(position['yPos']) + 1
            z = math.floor(position['zPos'])
            
            
            newHouse = houseFile.House(x, y, z, random.randint(5, 5), random.randint(6, 6), random.randint(3, 3), random.randint(1, 3), random.randint(1, 2)) 
            self.houses.append(newHouse)
            
        # Adds structures to the village.
        for each in self.extraLocations:
            selector = random.randint(0, 2)
            
            x = each['xPos']
            y = each['yPos']    
            z = each['zPos']    
                
            # outside stuff files        
            if selector == 0:   
                newGarden = gardenFile.Garden(x, y, z)
                self.extraStructures.append(newGarden)
                
            elif selector == 1:    
                newWell = wellFile.Well(x, y, z)
                self.extraStructures.append(newWell)
            
            elif selector == 2:
                newPlayground = playgroundFile.Playground(x, y, z)
                self.extraStructures.append(newPlayground)
        

    # This is used to get the border values of each piece of land.
    # This function is no longer in use but was originally used to prevent terraforming from ruining other houses.
    def getBorderVals(self):
        
        borderCoordinates = []
        
        for each in self.houseLocations:
            x = each['xPos']
            z = each['zPos']
            for i in range(-10, 10):
                borderCoordinates.append([x + i, z - 10])
                borderCoordinates.append([x + i, z + 10])
                borderCoordinates.append([x - 10, z + i])
                borderCoordinates.append([x + 10, z + i])
                
        self.landBorders = borderCoordinates
        
        
    # First terraforms the locations for each house and then terraforms for each extra structure.
    def terraformStructureLocations(self):
        mc = minecraft.Minecraft.create()
        
        borders = self.landBorders
        
        # Calls the terraform function for each house that belongs to this village.
        for each in self.houses:
            x = each.getx()
            z = each.getz()
            length = each.getLength()
            width = each.getWidth()
            
            heights = scanning.areaScan(x, z, width, length)
            
            y = max(heights)
            
            if mc.getBlock(x, y, z) == 8:
                y += 1
            
            each.sety(y)
            
            terrainFile.terraform(x, y, z, length, width, borders)
            
        # Calls the terrafrom function for each structure that belongs to this village.
        for each in self.extraStructures:
            
            x = each.getX()
            z = each.getZ()
            y = each.getY()
            
            if mc.getBlock(x, y, z) == 8:
                y += 1
            
            each.setY(y)
            
            if each.getType() == 'Garden':
                length = each.getLength() - 3
                width = each.getWidth() - 3
            
            elif each.getType() == 'Well':
                length = each.getLength() - 3
                width = each.getWidth() - 3

            elif each.getType() == 'Playground':
                length = each.getLength() - 2
                width = each.getWidth() - 2
                
            terrainFile.terraform(x, y, z, length, width, borders)
            
                            
    # Places each house that belongs to the village. 
    def placeHouses(self):
        for each in self.houses:
            each.generateHouse()
            
        # Finds and records the locations of each door. This is used for pathing to houses.
        doorPositions = []
        for house in newVillage.houses:
            #make the door position for path three blocks out
            door_position = house.doorPosition
            #house floor id = 98 which is stone brick
            #this code is trying to offset the door position for the path files to work, this is not a good solution and needs to be redone -Josh
            if house.doorFacing == 'N':
                doorPositions.append((door_position[0],door_position[2] - 3))
            elif house.doorFacing == 'S':
                doorPositions.append((door_position[0],door_position[2] + 3))
            elif house.doorFacing == 'E':
                doorPositions.append((door_position[0] + 3,door_position[2]))
            else:
                doorPositions.append((door_position[0] - 3,door_position[2]))
                
        self.doorPositions = doorPositions
            
        
    # places each extra structure that belongs to the village. Gardens, wells and playgrounds are children of structures.
    def placeExtras(self):
        for each in self.extraStructures:
            
            structure_type = each.getType()
            
            if structure_type == 'Garden':
                each.generateGarden()
            elif structure_type == 'Well':
                each.generateWell()
            elif structure_type == 'Playground':
                each.generatePlayground()

        

# Gets the players current position.
entityIds = mc.getPlayerEntityIds()
entityId1 = entityIds[0]
position = mc.entity.getPos(entityId1)

# Sets the number of houses and extra structures.
num_houses = 5
num_extra_structures = 2

# Centre coordinates for the village
x = math.floor(position.x)
y = math.floor(position.y)
z = math.floor(position.z)


# Generates the new village.
newVillage = Village(num_houses, num_extra_structures, x, y, z)

# Starts the village generation timer.
start = time.time()

# Functions for generating a village.
newVillage.generatePositions()
newVillage.generateVillage()
newVillage.getBorderVals()
newVillage.terraformStructureLocations()
newVillage.placeHouses()
newVillage.placeExtras()

# Generates the path connecting all houses.
pathFile.generatePath(newVillage.doorPositions, x, z)

# Ends the timer are posts the string to minecraft chat.
end = time.time()
mc.postToChat(f'Village complete. It took:{end - start: .2f} seconds')

            
    
