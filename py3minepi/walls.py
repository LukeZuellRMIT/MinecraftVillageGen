import random
import time
from mcpi import minecraft

#note: house length (z axis) range and house width (x axis)

#this function creates the exterior walls
def createWalls(houseLength, houseWidth, wallHeight, x, y, z, num):
    mc = minecraft.Minecraft.create()

    mc.setBlocks(x - houseWidth + 1, y, z - houseLength + 1, x - houseWidth + 1, y + wallHeight - 1, z + houseLength - 1, num)
    
    mc.setBlocks(x - houseWidth + 1, y, z - houseLength + 1, x + houseWidth - 1, y + wallHeight - 1, z - houseLength + 1, num)
    
    mc.setBlocks(x + houseWidth - 1, y, z + houseLength - 1, x + houseWidth - 1, y + wallHeight - 1, z - houseLength + 1, num)

    mc.setBlocks(x + houseWidth - 1, y, z + houseLength - 1, x - houseWidth + 1, y + wallHeight - 1, z + houseLength - 1, num)

#this function recursively builds the interior walls and returns a list of lists of all the x and z coordinates of where the walls lie on
def createInnerWalls(houseLength, houseWidth, wallHeight, x, floor_y, z, num, bearing, randomQuit, prevDoorPos, frontDoorPos):
    mc = minecraft.Minecraft.create()
    mc.postToChat(f'anchor x:{x} y:{floor_y} z:{z}')
    lists = [[]]
    
    #base case, random quit is a chance for the recursion to stop early which creates variation in wall design. It enables the house to have some larger rooms
    if randomQuit == 1:
        return None
    
    if bearing == 'S':
        #base case
        if houseWidth < 8:
            return None

        #find the middle x coordinate to split the room 
        middle_x = ((x - houseWidth + x) // 2) + random.randint(-1, 1)
        #ensuring that the middle x does not lie on an interior door or the front door. If it does then it creates a new middle x
        while middle_x == prevDoorPos[0] or ((z == frontDoorPos[2]or z + houseLength == frontDoorPos[2]) and middle_x == frontDoorPos[0]):
            middle_x = ((x - houseWidth + x) // 2) + random.randint(-1, 1)
        
        #create the wall, first setting out the starting xyz, and ending xyz, for readability.
        startCoor = (middle_x, floor_y, z)
        endCoor = (middle_x, floor_y + wallHeight, z + houseLength)
        mc.setBlocks(startCoor[0], startCoor[1], startCoor[2], endCoor[0], endCoor[1], endCoor[2], num)
        
        #create the door
        newprevDoorPos = (middle_x, floor_y, random.randint(startCoor[2] + 1, endCoor[2] - 1))
        mc.setBlocks(newprevDoorPos[0], newprevDoorPos[1], newprevDoorPos[2], newprevDoorPos[0], newprevDoorPos[1] + 1, newprevDoorPos[2], 0)
        
        #add torches
        mc.setBlock(newprevDoorPos[0] + 1, newprevDoorPos[1] + 2, newprevDoorPos[2], 50, 1)
        mc.setBlock(newprevDoorPos[0] - 1, newprevDoorPos[1] + 2, newprevDoorPos[2], 50, 2)

        #mc.postToChat(f'wall created SOUTH bound from x:{x1} y:{y1} z:{z1} ---->  x:{x2} y:{y2} z:{z2} with wall height {wallHeight}, house LENGTH: {houseLength}, house WIDTH {houseWidth}')
        
        #build the list of coordinates which the wall lies on, these will be the x and z coordinates
        for i in range(startCoor[2], endCoor[2] + 1):
            lists[0].append((middle_x, floor_y, i))
        
        #recursion call for the left half of the now split room. Adding onto the list of lists
        tempList = createInnerWalls(houseLength, x - middle_x, wallHeight, x, floor_y, z, num, 'W', random.randint(0, 5), newprevDoorPos, frontDoorPos)
        if tempList != None: lists += tempList
        #recursion call for the right half of the now split room. Adding onto the list of lists
        tempList = createInnerWalls(houseLength, middle_x - (x - houseWidth), wallHeight, middle_x, floor_y, z, num, 'W',random.randint(0, 5), newprevDoorPos, frontDoorPos)
        if tempList != None: lists += tempList
    else:
        #base case
        if (houseLength < 8):
            return None
        
        middle_z = ((z + (z + houseLength)) // 2) + random.randint(-1, 1)
        while middle_z == prevDoorPos[2] or ((x == frontDoorPos[0] or x - houseWidth == frontDoorPos[0]) and middle_z == frontDoorPos[2]):
            middle_z = ((2*z + houseLength) // 2) + random.randint(-1, 1)
        
        startCoor = (x, floor_y, middle_z)
        endCoor = (x - houseWidth, floor_y + wallHeight, middle_z)
        
        mc.setBlocks(startCoor[0], startCoor[1], startCoor[2], endCoor[0], endCoor[1], endCoor[2], num)
        
        #create the door
        newprevDoorPos = (random.randint(endCoor[0] + 1, startCoor[0] - 1), floor_y, middle_z)
        mc.setBlocks(newprevDoorPos[0], newprevDoorPos[1], newprevDoorPos[2], newprevDoorPos[0], newprevDoorPos[1] + 1, newprevDoorPos[2], 0)
        
        #add torches
        mc.setBlock(newprevDoorPos[0], newprevDoorPos[1] + 2, newprevDoorPos[2] - 1, 50, 4)
        mc.setBlock(newprevDoorPos[0], newprevDoorPos[1] + 2, newprevDoorPos[2] + 1, 50, 3)

        #mc.postToChat(f'wall created WEST bound from x:{x1} y:{y1} z:{z1} ---->  x:{x2} y:{y2} z:{z2} with wall height {wallHeight}, house LENGTH: {houseLength}, house WIDTH {houseWidth}')
        
        #build the list of coordinates which the wall lies on, these will be the x and z coordinates
        for i in range(endCoor[0], startCoor[0] + 1):
            lists[0].append((i, floor_y, middle_z))
        
        #Because middle_z - z is used to find a length, the number needs to be positive. In the case that coordinates are negative, the z2 - z1 needs to be positive
        temp = middle_z - z
        if temp < 0:
            temp = temp * -1
        
        #top half
        tempList = createInnerWalls(houseLength - temp, houseWidth, wallHeight, x, floor_y, middle_z, num, 'S',random.randint(0, 5), newprevDoorPos, frontDoorPos)
        if tempList != None: lists += tempList
        #bottom half
        tempList = createInnerWalls(temp, houseWidth, wallHeight, x, floor_y, z, num, 'S',random.randint(0, 5), newprevDoorPos, frontDoorPos)
        if tempList != None: lists += tempList
    #now return the list of lists
    return lists
