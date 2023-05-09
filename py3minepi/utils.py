import random
from mcpi import minecraft
from mcrcon import MCRcon
from time import sleep

mc = minecraft.Minecraft.create()

mcr = MCRcon("localhost", "123")
mcr.connect()


def generateStairs(houseLength, houseWidth, x, y, z, floors, stairBlock):
    mc.setBlocks(x - houseWidth + 2, y, z - houseLength + 2, x - houseWidth + 2, y + 3, z - houseLength + 2, 0)
    #print(x)
    #print(y)
    #print(z)
    # need help fixing :(
    if floors > 1:
        for i in range(floors):
            for j in range(1, 5):
                sleep(0.1)
                mc.setBlocks(x - houseWidth + 2 + j, y + j, z - houseLength + 2, x - houseWidth + 2 + j, y + 2 + j, z - houseLength + 2, 0)
                mc.setBlock(x - houseWidth + 2 + j, y + j - 1, z - houseLength + 2, stairBlock, 0)

    mcr.command(f"setblock {x - houseWidth + 4} {y} {z - houseLength + 2} minecraft:furnace[lit=true,facing=south]")
    
            #mc.setBlocks(x - houseWidth + 6, y + 4, z - houseLength + 2, x - houseWidth + 6, y + 6, z - houseLength + 2, 0)

def generateUtil(houseLength, houseWidth, x, y, z, wallPos):
    mc = minecraft.Minecraft.create()

    # picking random side
    def pickingForBlock(houseLength, houseWidth, x, y, z, wallPos, block):
        # stopper for while loop
        # stop = 0
        
        # while stop != 1:
        #     # chooses random side to place block ect
        #     randomSide = random.randint(1, 4)
        #     randomSide = 1
        #     # south side
        #     if randomSide == 1:
        #         # chooses random spot on x side
        #         randomx = random.randint(x - houseWidth + 2, x + houseWidth - 2)
        #         # gets down the wall pos array
        #         print(wallPos)
        #         for i in wallPos:
        #             #print(wallPos)
        #             print(i)
        #             blockCoord = [randomx, z + houseLength - 2]
        #             #print(blockCoord[0])
        #             #print(blockCoord[1])
        #             print(blockCoord)
                    
        #             if blockCoord == i:
        #                 print('no can do')
        #                 stop = 1
        #                 break
        #             else:
        #                 continue
        #             break
        #         break
        #     mc.setBlock(blockCoord[0], y, blockCoord[1], block)
        #     stop = 1
        pass

    # crafting table
    pickingForBlock(houseLength, houseWidth, x, y, z, wallPos, 58)

    #randomx = random.randint(x - houseWidth + 2, x + houseWidth - 2)
    #randomy = random.randint(y - houseLength + 2, y + houseLength - 2)
    #if mc.getBlock(randomx, y, randomy):
    #print(mc.getBlock(x + houseWidth - 2, y, z + houseLength - 2))
    #if mc.getBlock(x + houseWidth - 2, y, z + houseLength - 2) != NONE:

    #mc.setBlock(x + houseWidth - 2, y, z + houseLength - 2, 26, 11) # head of bed
    #mc.setBlock(x + houseWidth - 3, y, z + houseLength - 2, 26, 3) # feed of bed
    #mcr.command(f"setblock {x + houseWidth - 4} {y} {z + houseLength - 2} minecraft:furnace[lit=true,facing=north]") # on furance
    #mc.setBlock(x + houseWidth - 5, y, z + houseLength - 2, 58) # craft table
    #tempx = x + houseWidth - 6
    #tempy = y
    #tempz = z + houseLength - 2
    #mcr.command("""setblock """ + str(tempx) + " " + str(tempy) + " " + str(tempz) + """ minecraft:chest[type=left]{Items:[{Slot:0b,id:"minecraft:diamond_helmet",Count:1b},{Slot:1b,id:"minecraft:diamond_chestplate",Count:1b},{Slot:2b,id:"minecraft:diamond_leggings",Count:1b},{Slot:3b,id:"minecraft:diamond_boots",Count:1b},{Slot:4b,id:"minecraft:cooked_beef",Count:64b},{Slot:5b,id:"minecraft:golden_apple",Count:64b},{Slot:9b,id:"minecraft:diamond_sword",Count:1b},{Slot:10b,id:"minecraft:diamond_pickaxe",Count:1b},{Slot:11b,id:"minecraft:diamond_axe",Count:1b},{Slot:12b,id:"minecraft:diamond_shovel",Count:1b}]} replace""")
    #mcr.command(f"setblock {x + houseWidth - 7} {y} {z + houseLength - 2} minecraft:chest[type=left]") # on furance
