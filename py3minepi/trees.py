import threading
from mcpi import minecraft
import time

import concurrent.futures

mc = minecraft.Minecraft.create()

# this algorithm is quite convoluted as it was my first forray into multi-threading
# (I added the threading after the function was made, hence why there are so many splintered sub functions.)
# - Mark

# RemoveTree is the main function. It creates the initial 2 threads which iterates over the positive
# and negative x values from the position that the tree was found. There are some checks that are done to find which
# direction the algorithm needs to move in.
def removeTree(initialX, initialZ):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    start = time.time()

    mc = minecraft.Minecraft.create()
    
    mc.postToChat('Remove Tree has been called')
    
    x = initialX
    z = initialZ
    
    # Initialises checks in both x and z directions to negative
    negativeXCheck = False
    positiveXCheck = False
    
    negativeZCheck = False
    positiveZCheck = False
    
    
    # Determines whether or not there is a tree block in each direction.
    blockHeight = mc.getHeight(x - 1, z)
    blockID = mc.getBlock(x - 1, blockHeight, z)
    if blockID in tree_blocks:
        negativeXCheck = True
        
    blockHeight = mc.getHeight(x + 1, z)
    blockID = mc.getBlock(x + 1, blockHeight, z)
    if blockID in tree_blocks:
        positiveXCheck = True
        
        
    blockHeight = mc.getHeight(x, z - 1)
    blockID = mc.getBlock(x, blockHeight, z - 1)
    if blockID in tree_blocks:
        negativeZCheck = True
        
    blockHeight = mc.getHeight(x, z + 1)
    blockID = mc.getBlock(x, blockHeight, z + 1)
    if blockID in tree_blocks:
        positiveZCheck = True
        
    
    # If both x directions are false a check is done again in each z direction to find where the tree starts.
    if negativeXCheck == False and positiveXCheck == False:
        if positiveZCheck == True:
            
            blockHeight = mc.getHeight(x - 1, z + 1)
            blockID = mc.getBlock(x - 1, blockHeight, z + 1)
            if blockID in tree_blocks:
                negativeXCheck = True
                
                
            blockHeight = mc.getHeight(x + 1, z + 1)
            blockID = mc.getBlock(x + 1, blockHeight, z + 1)
            if blockID in tree_blocks:
                positiveXCheck = True
                
            initialZ += 1
            
        elif negativeZCheck == True:

            blockHeight = mc.getHeight(x - 1, z - 1)
            blockID = mc.getBlock(x - 1, blockHeight, z - 1)
            if blockID in tree_blocks:
                negativeXCheck = True
                
                
            blockHeight = mc.getHeight(x + 1, z - 1)
            blockID = mc.getBlock(x + 1, blockHeight, z - 1)
            if blockID in tree_blocks:
                positiveXCheck = True
            
            initialZ -= 1
    
    
    # starts the thread for each x direction. Prevents the code from waiting for the negativeXloop to finish before starting the positiveXloop
    negativeXThread = threading.Thread(target=negativeXloop, args=(initialX, negativeXCheck, initialZ))
    negativeXThread.start()
            
    positiveXThread = threading.Thread(target=positiveXloop, args=(initialX, positiveXCheck, initialZ))
    positiveXThread.start()
    
    negativeXThread.join()
    positiveXThread.join()
    
    
    # posts the time the tree removal took to the minecraft chat.
    end = time.time()
    mc.postToChat(f'tree removal complete. It took:{end - start: .2f} seconds')
                   

# positiveXloop is the function that iterates over the values in the positive x direction. It creates threads calling positiveXfunction. This function also does checks 
# in the positive and negative z directions to check if any leaves have been left behind.
def positiveXloop(initialX, positiveXCheck, initialZ):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    mc = minecraft.Minecraft.create()
    
    x = initialX
    
    PXthreads = []
    num_iterations = 0
    
    # Removes the tree for the values in positive x direction.
    # num_iterations is used to prevent the algorithm from running uncontrolled in large forests.
    # 7 was chosen as this is generally the maximum width of a tree.
    while positiveXCheck and num_iterations < 7:
        
        # Starts new thread to check every postive X position.
        t = threading.Thread(target=positiveXfunction, args=(x, initialZ))
        t.start()
        PXthreads.append(t)
        
        x += 1
        z = initialZ
        blockHeight = mc.getHeight(x, z)
        blockID = mc.getBlock(x, blockHeight, z)
        
        if blockID in tree_blocks:
            positiveXCheck = True
        else:
            i = 1
            treeFound = False
            
            # Some trees have leaves that are seperated by more then 1 z values. 
            # This check 4 more in each direction if none are found initially.
            # while i < 4:
            #     blockHeight = mc.getHeight(x, z + i)
            #     blockID = mc.getBlock(x, blockHeight, z + i)
            #     if blockID in tree_blocks:
            #         initialZ = z + i
            #         treeFound = True
            #         continue
            #         i = 5
            #     else:
            #         i += 1
            
            # i = 1     
            # while i < 4:
            #     blockHeight = mc.getHeight(x, z - i)
            #     blockID = mc.getBlock(x, blockHeight, z - i)
            #     if blockID in tree_blocks:
            #         initialZ = z - i
            #         treeFound = True
            #         continue
            #         i = 4
            #     else:
            #         i += 1
            
            positiveXCheck = treeFound
        num_iterations += 1
    
    
    for thread in PXthreads:
        thread.join()
            

# negativeXloop is the function that iterates over the values in the negative x direction. It creates threads calling negativeXfunction. This function also does checks 
# in the negative and negative z directions to check if any leaves have been left behind.
def negativeXloop(initialX, negativeXCheck, initialZ):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    mc = minecraft.Minecraft.create()
    x = initialX
    
    NXthreads = []
    num_iterations = 0
    
    # removes the tree for values in the negative x direction
    # num_iterations is used to prevent the algorithm from running uncontrolled in large forests.
    # 7 was chosen as this is generally the maximum width of a tree.
    while negativeXCheck and num_iterations < 7:
        
        # Starts new thread to check every postive X position.
        t = threading.Thread(target=negativeXfunction, args=(x, initialZ))
        t.start()
        NXthreads.append(t)
        
        x -= 1
        z = initialZ
        blockHeight = mc.getHeight(x, z)
        blockID = mc.getBlock(x, blockHeight, z)
        if blockID in tree_blocks:
            negativeXCheck = True
        else:
            i = 1
            treeFound = False
            
            # Some trees have leaves that are seperated by more then 1 z values. 
            # This check 4 more in each direction if none are found initially.
            # while i < 4:
            #     blockHeight = mc.getHeight(x, z + i)
            #     blockID = mc.getBlock(x, blockHeight, z + i)
            #     if blockID in tree_blocks:
            #         initialZ = z + i
            #         treeFound = True
            #         i = 5
            #     else:
            #         i += 1
            
            # i = 1     
            # while i < 4:
            #     blockHeight = mc.getHeight(x, z - i)
            #     blockID = mc.getBlock(x, blockHeight, z - i)
            #     if blockID in tree_blocks:
            #         initialZ = z - i
            #         treeFound = True
            #         i = 4
            #     else:
            #         i += 1
            
            negativeXCheck = treeFound
        num_iterations += 1
            
    
    for thread in NXthreads:
        thread.join()         
            
            
# This function calls the positive and negative z checks in the negative x direction. (it moves sideways calling functions that destroy everything in z directions.)
def negativeXfunction(x, initialZ):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    mc = minecraft.Minecraft.create()
    z = initialZ
    
    negativeZCheck = False
    positiveZCheck = False

    blockHeight = mc.getHeight(x, z - 1)
    blockID = mc.getBlock(x, blockHeight, z - 1)
    if blockID in tree_blocks:
        negativeZCheck = True
        NZCheck = threading.Thread(target=NZchecks, args=(negativeZCheck, x, z))
        NZCheck.start()
        

    z = initialZ 
    
    blockHeight = mc.getHeight(x, z + 1)
    blockID = mc.getBlock(x, blockHeight, z + 1)
    if blockID in tree_blocks:
        positiveZCheck = True
        PZCheck = threading.Thread(target=PZchecks, args=(positiveZCheck, x, z))
        PZCheck.start()
        

    if negativeZCheck:
        NZCheck.join()
    if positiveZCheck:
        PZCheck.join()


# This function calls the positive and negative z checks in the positive x direction. (it moves sideways calling functions the destroy everything in z directions.)
def positiveXfunction(x, initialZ):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    mc = minecraft.Minecraft.create()
    z = initialZ
    
    negativeZCheck = False
    positiveZCheck = False
    
    blockHeight = mc.getHeight(x, z - 1)
    blockID = mc.getBlock(x, blockHeight, z - 1)
    if blockID in tree_blocks:
        negativeZCheck = True
        NZCheck = threading.Thread(target=NZchecks, args=(negativeZCheck, x, z))
        NZCheck.start()
        
    
    z = initialZ
    
    blockHeight = mc.getHeight(x, z + 1)
    blockID = mc.getBlock(x, blockHeight, z + 1)
    if blockID in tree_blocks:
        positiveZCheck = True
        PZCheck = threading.Thread(target=PZchecks, args=(positiveZCheck, x, z))     
        PZCheck.start()
    
        
    if negativeZCheck:
        NZCheck.join()
    if positiveZCheck:
        PZCheck.join()

    
# NZchecks runs in the negative z direction. It checks if the block is part of a tree and if it is
# it calls placeAirColumn which removes all tree parts in the (x,z) position.
def NZchecks(negativeZCheck, x, z):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    
    mc = minecraft.Minecraft.create()
    
    threadArgs = []
    num_iterations = 0
    
    while negativeZCheck and num_iterations < 7:
        
        threadArgs.append([x, z])
        
        z -= 1
        blockHeight = mc.getHeight(x, z)
        blockID = mc.getBlock(x, blockHeight, z)
        if blockID in tree_blocks:
            negativeZCheck = True
        else:
            negativeZCheck = False
            
        num_iterations += 1
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        
        airBlocks = executor.map(placeAirColumn, threadArgs)
        
            

# PZchecks runs in the positive z direction. It checks if the block is part of a tree and if it is
# it calls placeAirColumn which removes all tree parts in the (x,z) position.            
def PZchecks(positiveZCheck, x, z):
    tree_blocks = [18, 161, 17, 162, 99, 100]
    
    mc = minecraft.Minecraft.create()

    threadArgs = []
    num_iterations = 0
    
    while positiveZCheck and num_iterations < 7:
        
        threadArgs.append([x, z])
        
        z += 1
        blockHeight = mc.getHeight(x, z)
        blockID = mc.getBlock(x, blockHeight, z)
        if blockID in tree_blocks:
            positiveZCheck = True
        else:
            positiveZCheck = False
            
        num_iterations += 1
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        
        airBlocks = executor.map(placeAirColumn, threadArgs)


# This iterates over the y posititions for a given set of (x,z) coordinates. 
# It stops when the highest block is no longer part of a tree.
def placeAirColumn(args):
    
    x = args[0]
    z = args[1]
    
    tree_blocks = [18, 161, 17, 162, 99, 100]
    mc = minecraft.Minecraft.create()
    
    blockHeight = mc.getHeight(x, z)
    blockID = mc.getBlock(x, blockHeight, z)
    while blockID in tree_blocks:
        
        mc.setBlock(x, blockHeight, z, 0)
        
        
        blockHeight = mc.getHeight(x, z)
        blockID = mc.getBlock(x, blockHeight, z)






