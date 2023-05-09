import threading
import random
from mcpi import minecraft
import operator
import time

import trees as treeDestroyer


# Main function that branches off to east, west and north south functions.
def terraform(centerX, centerY, centerZ, length, width, borders):
    
    mc = minecraft.Minecraft.create()
        
    baseBlock = mc.getBlock(centerX, centerY - 2, centerZ)
        
    # sets dirt block to grass block
    if baseBlock == 3:
        baseBlock = 2
    
    # Sets sand block to sand stone
    if baseBlock == 12:
        baseBlock = 24
        
    # Sets gravel to stone
    if baseBlock == 13:
        baseBlock = 1
    
    # Sets air to stone
    if baseBlock == 0:
        baseBlock = 1
        
    # sets still and flowing water to stone
    if baseBlock == 9 or baseBlock == 8:
        baseBlock = 1
    
    
    # Clears land dirrectly abover build site
    mc.setBlocks(centerX - width - 2, centerY, centerZ - length - 2, centerX + width + 2, centerY + 25, centerZ + length + 2, 0)
    
    # makes base of house one solid block
    mc.setBlocks(centerX - width - 2, centerY - 1, centerZ - length - 2, centerX + width + 2, centerY - 1, centerZ + length + 2, baseBlock)
    
    
    xThreads = []
    # Fills in the ground under a house with a random assortment of stone, coal and iron.
    for i in range(- width - 2, width + 3):
        curX = centerX + i
        
        t = threading.Thread(target=Xiteration, args=(curX, length, centerZ, centerY, baseBlock))
        t.start()
        xThreads.append(t)
    
        
    for thread in xThreads:
        thread.join()
                    
    
    ops = {
        "+": operator.add,
        "-": operator.sub,
    }  

    # Smooths east and west sections of terrain
    # Records the amount of blocks that have been terraformed and passes it back through lists.
    eastResults = []
    westResults = []
    ESThreads = []
    for k in range(2): 
        
        # Changes which way the terraforming algorithm is going to run.
        Z_func = ops["+"]
        X_func = ops["-"]
        X2_func = ops["+"]
        
        if k == 1:
            Z_func = ops["+"]
            X_func = ops["+"]
            X2_func = ops["-"]
    
        # runs the eastwestsmoothing on its own thread. This enables east and west side to be terrafromed simultaneously.
        t = threading.Thread(target=eastWestSmoothing, args=(centerX, centerZ, width, length, Z_func, X_func, X2_func, baseBlock, k, eastResults, westResults, borders))
        t.start()
        ESThreads.append(t)
        
    for thread in ESThreads:
        thread.join()
        
        
    # Checks what distance from the house was terraformed. This enables the south west iterations to cover a wider area to ensure that corners 
    # are terraformed.
    numEast = eastResults[0]
    numEast.sort(reverse=True)
    
    numWest = westResults[0]
    numWest.sort(reverse=True)

    extraEast = numEast[0]
    extraWest = numWest[0]
        
        
    # Smooths North and South sections of terrain.
    NSThreads = []
    for k in range(2): 
        
        # Changes which way the terraforming algorithm is going to run.
        Z_func = ops["-"]
        Z2_func = ops["+"]
        X_func = ops["+"]
        
        if k == 1:
            Z_func = ops["+"]
            Z2_func = ops["-"]
            X_func = ops["+"]
        
        # runs northsouthsmoothing on individual threads so that north and south can terraform at the same time. 
        t = threading.Thread(target=northSouthSmoothing, args=(centerX, centerZ, width, length, Z_func, X_func, Z2_func, baseBlock, k, extraEast, extraWest, borders))
        t.start()
        NSThreads.append(t)
        
    for thread in NSThreads:
        thread.join()


# Calls EWiteration for each row of blocks that must be terraformed.
def eastWestSmoothing(centerX, centerZ, width, length, Z_func, X_func, X2_func, baseBlock, k, eastResults, westResults, borders):
    mc = minecraft.Minecraft.create() 
    
    x = centerX - width - 2
    z = centerZ - length - 2
    
    if k == 1:
        x = centerX + width + 2 
        z = centerZ - length - 2
    
    # Initialises the array of results that will be populated from then return values of EWiteration threads
    newResults = [None] * (2 * length + 6)
    EWSmoothingThreads = []
    for j in range (2 * length + 6):
        t = threading.Thread(target=EWiteration, args=(x, z, j, X_func, X2_func, Z_func, baseBlock, newResults, borders))
        t.start()
        EWSmoothingThreads.append(t)
    
    
    # Populates the array with results from EWiteration
    # These results are used to determine how wide the North south smoothing section must run to cover all terraformed land.
    for thread in EWSmoothingThreads:
        thread.join()
        if k == 1:
            westResults.append(newResults)  
        else:
            eastResults.append(newResults)      
        
        

# Checks the block height differences and edits the terrain.
def EWiteration(x, z, j, X_func, X2_func, Z_func, baseBlock, newResults, borders):
    mc =minecraft.Minecraft.create()
    
    done = 0
    i = 1
    
    downwardThreads = []
    
    currentDirection= ''
    
    while done != 1:
        
        noUpdates = 1
        
        # Previous blockHeight:
        previousHeight = mc.getHeight(X_func(X2_func(x, 1), i), Z_func(z, j))
        
        # Next block height
        currentHeight = mc.getHeight(X_func(x, i), Z_func(z, j))
        
        blockID = mc.getBlock(X_func(x, i), currentHeight, Z_func(z, j)) 
        if (blockID == 18) or (blockID == 161) or (blockID == 17) or (blockID == 162):
            treeDestroyer.removeTree(X_func(x, i), Z_func(z, j))
            currentHeight = mc.getHeight(X_func(x, i), Z_func(z, j))
            
        blockID = mc.getBlock(X_func(x, i), currentHeight, Z_func(z, j)) 
        
        if blockID == 8 or blockID == 9:
            blockID = 1
            
        bottomBlockID = blockID
        
        if bottomBlockID == 2:
            bottomBlockID = 3
            
        # checks current height between current and previous block
        # Executes if terrain going up
        if currentHeight - previousHeight > 1:
            
            # Stops the algorithm once a change in terraforming direction has been detected.
            if currentDirection == '' or currentDirection == 'Upwards':
                currentDirection = 'Upwards'
            else:
                break

            randomHeight = random.randint(1,10)

            mc.setBlocks(X_func(x, i), previousHeight + 1, Z_func(z, j), X_func(x, i), currentHeight + 1, Z_func(z, j), 0)
            
            if randomHeight < 3:
                mc.setBlock(X_func(x, i), previousHeight + 1, Z_func(z, j), blockID)
                mc.setBlock(X_func(x, i), previousHeight, Z_func(z, j), bottomBlockID)
            elif randomHeight < 7:
                mc.setBlock(X_func(x, i), previousHeight + 2, Z_func(z, j), blockID)
                mc.setBlock(X_func(x, i), previousHeight + 1, Z_func(z, j), bottomBlockID)
                mc.setBlock(X_func(x, i), previousHeight, Z_func(z, j), bottomBlockID)
            else:
                mc.setBlock(X_func(x, i), previousHeight + 3, Z_func(z, j), blockID)
                mc.setBlock(X_func(x, i), previousHeight + 2, Z_func(z, j), bottomBlockID)
                mc.setBlock(X_func(x, i), previousHeight + 1, Z_func(z, j), bottomBlockID)
                mc.setBlock(X_func(x, i), previousHeight, Z_func(z, j), blockID)
            
            noUpdates = 0
            
        
        # Checks height difference between current and previos block.
        # Executes if terrain going down
        if previousHeight - currentHeight > 1:
            
            randomHeight = random.randint(1,10)
            
            if currentDirection == '' or currentDirection == 'Downwards':
                currentDirection = 'Downwards'
            else:
                break
            
            if randomHeight < 2:
                mc.setBlock(X_func(x, i), previousHeight - 1, Z_func(z, j), baseBlock)
                
                t = threading.Thread(target=Jiteration, args=(X_func(x, i), previousHeight - 2, Z_func(z, j), bottomBlockID))
                t.start()
                downwardThreads.append(t)
                
            elif randomHeight < 7:
                mc.setBlock(X_func(x, i), previousHeight - 2, Z_func(z, j), baseBlock)
                
                t = threading.Thread(target=Jiteration, args=(X_func(x, i), previousHeight - 3, Z_func(z, j), bottomBlockID))
                t.start()
                downwardThreads.append(t)
                
            else:
                mc.setBlock(X_func(x, i), previousHeight - 3, Z_func(z, j), baseBlock)
                mc.setBlock(X_func(x, i), previousHeight - 4, Z_func(z, j), bottomBlockID)
                
                t = threading.Thread(target=Jiteration, args=(X_func(x, i), previousHeight - 5, Z_func(z, j), bottomBlockID))
                t.start()
                downwardThreads.append(t)
            
            noUpdates = 0
        
        i += 1
        done = noUpdates
    
    for thread in downwardThreads:
        thread.join()
        
    newResults[j] = i
    # print('EWIteration: ', j, 'thread: ', newResults[j])
        

# Calls NSiteration for each row of blocks that must be terraformed.
def northSouthSmoothing(centerX, centerZ, width, length, Z_func, X_func, Z2_func, baseBlock, k, extraEast, extraWest, borders):

    x = centerX - width - 2
    z = centerZ - length - 2 
    
    if k == 1:
        x = centerX - width - 2
        z = centerZ + length + 2


    NSSmoothingThreads = []
    # get number of blocks terraformed by EWiterations
    for j in range (-extraEast, 2 * width + 6 + extraWest):
        t = threading.Thread(target=NSiteration, args=(x, z, j, X_func, Z_func, Z2_func, baseBlock, borders))
        t.start()
        NSSmoothingThreads.append(t)
        
    
    
    for thread in NSSmoothingThreads:
        thread.join()
                    

# Checks the block height differences and edits the terrain
def NSiteration(x, z, j, X_func, Z_func, Z2_func, baseBlock, borders):
    mc = minecraft.Minecraft.create()
    
    i = 1
    done = 0
    
    downwardThreads = []
    
    currentDirection = ''
    
    while done != 1:
        
        noUpdates = 1
        
        # Previous blockHeight:
        previousHeight = mc.getHeight(X_func(x, j), Z_func(Z2_func(z, 1), i))
        
        # Next block height
        currentHeight = mc.getHeight(X_func(x, j), Z_func(z, i))
        
        blockID = mc.getBlock(X_func(x, j), currentHeight, Z_func(z, i)) 
        if (blockID == 18) or (blockID == 161) or (blockID == 17) or (blockID == 162):
            treeDestroyer.removeTree(X_func(x, j), Z_func(z, i))
            currentHeight = mc.getHeight(X_func(x, j), Z_func(z, i))
        
        blockID = mc.getBlock(X_func(x, j), currentHeight, Z_func(z, i)) 
        
        if blockID == 8 or blockID == 9:
            blockID = 1
        
        bottomBlockID = blockID
        
        if bottomBlockID == 2:
            bottomBlockID = 3
        
        # checks current height between current and previous block
        # Executes if terrain going up
        if currentHeight - previousHeight > 1:
            
            # Stops the algorithm once a change in terraforming direction has been detected.
            if currentDirection == '' or currentDirection == 'Upwards':
                currentDirection = 'Upwards'
            else:
                break
        
            randomHeight = random.randint(1,10)

            mc.setBlocks(X_func(x, j), previousHeight + 1, Z_func(z, i), X_func(x, j), currentHeight + 1, Z_func(z, i), 0)
            
            if randomHeight < 3:
                mc.setBlock(X_func(x, j), previousHeight + 1, Z_func(z, i), blockID)
                mc.setBlock(X_func(x, j), previousHeight, Z_func(z, i),  bottomBlockID)
            if randomHeight < 7:
                mc.setBlock(X_func(x, j), previousHeight + 2, Z_func(z, i), blockID)
                mc.setBlock(X_func(x, j), previousHeight + 1, Z_func(z, i),  bottomBlockID)
                mc.setBlock(X_func(x, j), previousHeight, Z_func(z, i),  bottomBlockID)
            else:
                mc.setBlock(X_func(x, j), previousHeight + 3, Z_func(z, i), blockID)
                mc.setBlock(X_func(x, j), previousHeight + 2, Z_func(z, i),  bottomBlockID)
                mc.setBlock(X_func(x, j), previousHeight + 1, Z_func(z, i),  bottomBlockID)
                mc.setBlock(X_func(x, j), previousHeight, Z_func(z, i),  bottomBlockID)
            
            noUpdates = 0
            
        # Checks height difference between current and previos block.
        # Executes if terrain going down
        if previousHeight - currentHeight > 1:
            
            # Stops the algorithm once a change in terraforming direction has been detected.
            if currentDirection == '' or currentDirection == 'Downwards':
                currentDirection = 'Downwards'
            else:
                break

            randomHeight = random.randint(1,10)
        
            if randomHeight < 2:
                mc.setBlock(X_func(x, j), previousHeight - 1, Z_func(z, i), baseBlock)
                
                t = threading.Thread(target=Jiteration, args=(X_func(x, j), previousHeight - 2, Z_func(z, i), bottomBlockID))
                t.start()
                downwardThreads.append(t)
            
            elif randomHeight < 7:
                mc.setBlock(X_func(x, j), previousHeight - 2, Z_func(z, i), baseBlock)
                
                t = threading.Thread(target=Jiteration, args=(X_func(x, j), previousHeight - 3, Z_func(z, i), bottomBlockID))
                t.start()
                downwardThreads.append(t)
                
            else:
                mc.setBlock(X_func(x, j), previousHeight - 3, Z_func(z, i), baseBlock)
                mc.setBlock(X_func(x, j), previousHeight - 4, Z_func(z, i), bottomBlockID)
                
                t = threading.Thread(target=Jiteration, args=(X_func(x, j), previousHeight - 5, Z_func(z, i), bottomBlockID))
                t.start()
                downwardThreads.append(t)
                
            noUpdates = 0
        
        i += 1
        done = noUpdates
        
    for thread in downwardThreads:
        thread.join()

# Xiteration is called by teraform land, it iterates over every x block and calls j iteration.
def Xiteration(curX, length, centerZ, centerY, baseBlock):
    jThreads = []
    for j in range(- length - 2, length + 3):
        curZ = centerZ + j
        
        curY = centerY - 2
        
        t = threading.Thread(target=Jiteration, args=(curX, curY, curZ, baseBlock))
        t.start()
        jThreads.append(t)
    
    for thread in jThreads:
        thread.join()
        

# iterates over every y block and fills in any airblocks until it reaches the ground.
def Jiteration(curX, curY, curZ, baseBlock):
    mc = minecraft.Minecraft.create()
    airCheck = False
    
    blockID = mc.getBlock(curX, curY, curZ)
    
    # Checks for air, grasses and flowers, and snow
    if blockID == 0 or blockID == 31 or blockID == 175 or blockID == 78:
        airCheck = True
    
    # If block is grass replace with dirt.
    # This is done to prevent layering of grass blocks.
    if baseBlock == 2:
        baseBlock = 3
    
    while airCheck:
        
        blockInt = random.randint(1, 21)
        randomBlock = 0
        
        if blockInt <= 12:
            randomBlock = baseBlock
        elif blockInt <= 18:
            randomBlock = 1 # Stone
        elif blockInt == 19 or blockInt == 20:
            randomBlock = 16 # Iron
        elif blockInt == 21:
            randomBlock = 15 # coal
            
        mc.setBlock(curX, curY, curZ, randomBlock)
    
        curY -= 1
        
        blockID = mc.getBlock(curX, curY, curZ)
        
        # Checks for air, grasses and flowers, and snow
        if blockID == 0 or blockID == 31 or blockID == 175 or blockID == 78:
            airCheck = True
        else:
            airCheck = False