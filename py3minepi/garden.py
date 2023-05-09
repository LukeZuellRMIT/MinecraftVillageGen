from mcpi import minecraft
from mcrcon import MCRcon
from Structures import Structures 

mcr = MCRcon("localhost", "123")
mcr.connect()


class Garden(Structures):
    
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 10, 10, 'Garden')
        
        
    
    def generateGarden(self):
        mc = minecraft.Minecraft.create()
        
        x = self.x - 15
        y = self.y
        z = self.z

        
        while mc.getBlock(x + 19, y - 1, z) == 0:
            y -= 1
        

        # anchor spot :  this is x - 15 from the center of the garden
        # mc.setBlock(x , y, z, 1)

        y += 1
        
        # foundation
        mc.setBlocks(x + 6, y - 4, z - 9, x + 24, y + 7, z + 9, 0) # clearing space for garden
        mc.setBlocks(x + 6, y - 4, z - 9, x + 24, y - 3, z + 9, 1) # base
        mc.setBlocks(x + 6, y - 2, z - 9, x + 24, y - 1, z, 2) # pathway side
        mc.setBlocks(x + 14, y - 2, z + 9, x + 24, y - 1, z + 1, 12) # desert corner
        
        # next 4 lines are desert blending
        mc.setBlocks(x + 16, y - 1, z, x + 21, y - 1, z, 12)
        mc.setBlocks(x + 18, y - 1, z - 1, x + 20, y - 1, z - 1, 12)
        mc.setBlock(x + 19, y - 1, z - 2, 12)
        mc.setBlock(x + 23, y - 1, z + 1, 2)
        mc.setBlocks(x + 6, y - 2, z + 9, x + 13, y - 1, z + 1, 2) # pond corner

        


        # arches
        for i in range(0, 15, 14):
            mc.setBlock(x + 8 + i, y + 1, z - 6, 139) # stone fence for bottom left
            mc.setBlock(x + 8 + i, y + 1, z - 2, 139) # stone fence for bottom right
            mc.setBlocks(x + 8 + i, y + 4, z - 6, x + 8 + i, y + 5, z - 2, 96) # trap doors for top
            mc.setBlocks(x + 8 + i, y + 2, z - 6, x + 8 + i, y + 4, z - 6, 85) # left pillar
            mc.setBlocks(x + 8 + i, y + 2, z - 2, x + 8 + i, y + 4, z - 2, 85) # right pillar
            mc.setBlock(x + 8 + i, y + 4, z - 5, 85) # left fence
            mc.setBlock(x + 8 + i, y + 4, z - 3, 85) # right fence
            mc.setBlock(x + 8 + i, y + 4, z - 4, 107, 1) # middle gate
            mc.setBlocks(x + 7 + i, y + 4, z - 6, x + 7 + i, y + 4, z - 2, 1) # updating top fence data
            mc.setBlocks(x + 7 + i, y + 4, z - 6, x + 7 + i, y + 4, z - 2, 0) # updating top fence data
            mc.setBlock(x + 8 + i, y, z - 6, 17) # ground left
            mc.setBlock(x + 8 + i, y, z - 2, 17) # ground right
        

        # perimeter
        mc.setBlocks(x + 6, y - 4, z - 9, x + 24, y - 1, z - 9, 98) # north
        mc.setBlocks(x + 6, y - 4, z + 9, x + 24, y - 1, z + 9, 98) # south
        mc.setBlocks(x + 6, y - 4, z - 9, x + 6, y - 1, z + 9, 98) # west
        mc.setBlocks(x + 24, y - 4, z - 9, x + 24, y - 1, z + 9, 98) # east
        
        #corner-stones
        mc.setBlocks(x + 6, y - 4, z - 9, x + 6, y - 1, z - 9, 98, 3) #
        mc.setBlocks(x + 24, y - 4, z - 9, x + 24, y - 1, z - 9, 98, 3) #
        mc.setBlocks(x + 6, y - 4, z + 9, x + 6, y - 1, z + 9, 98, 3) #
        mc.setBlocks(x + 24, y - 4, z + 9, x + 24, y - 1, z + 9, 98, 3) 
        mc.setBlocks(x + 6, y - 4, z - 2, x + 6, y - 1, z - 2, 98, 3)
        mc.setBlocks(x + 6, y - 4, z - 6, x + 6, y - 1, z - 6, 98, 3)
        mc.setBlocks(x + 24, y - 4, z - 2, x + 24, y - 1, z - 2, 98, 3)
        mc.setBlocks(x + 24, y - 4, z - 6, x + 24, y - 1, z - 6, 98, 3)
        
        # pathway
        mc.setBlocks(x + 6, y - 1, z - 5, x + 9, y - 1, z - 3, 208) # west arch
        mc.setBlocks(x + 24, y - 1, z - 5, x + 21, y - 1, z - 3, 208) # east arch
        mc.setBlocks(x + 10, y - 1, z - 7, x + 10, y - 1, z - 4, 208)
        mc.setBlocks(x + 11, y - 1, z - 8, x + 11, y - 1, z - 5, 208)
        mc.setBlocks(x + 12, y - 1, z - 7, x + 12, y - 1, z - 4, 208)
        mc.setBlocks(x + 13, y - 1, z - 6, x + 13, y - 1, z - 3, 208)
        mc.setBlocks(x + 14, y - 1, z - 7, x + 14, y - 1, z - 2, 208)
        mc.setBlocks(x + 15, y - 1, z - 8, x + 15, y - 1, z - 2, 208) # middle
        mc.setBlocks(x + 16, y - 1, z - 7, x + 16, y - 1, z - 2, 208)
        mc.setBlocks(x + 17, y - 1, z - 6, x + 17, y - 1, z - 3, 208)
        mc.setBlocks(x + 18, y - 1, z - 7, x + 18, y - 1, z - 4, 208)
        mc.setBlocks(x + 19, y - 1, z - 8, x + 19, y - 1, z - 5, 208)
        mc.setBlocks(x + 20, y - 1, z - 7, x + 20, y - 1, z - 4, 208)


        # stairs into pond
        mc.setBlocks(x + 15, y - 1, z - 1, x + 14, y - 1, z - 1, 134, 3)


        # pond (lines grouped by z coord from north to south)

        mc.setBlocks(x + 15, y - 1, z, x + 14, y - 1, z, 8) # water
        mc.setBlocks(x + 15, y - 2, z, x + 14, y - 2, z, 12) # sand floor

        mc.setBlocks(x + 16, y - 1, z + 1, x + 13, y - 1, z + 1, 8) # water

        mc.setBlocks(x + 15, y - 1, z + 2, x + 15, y - 1, z + 2, 8) # water
        mc.setBlocks(x + 14, y - 1, z + 2, x + 12, y - 2, z + 2, 8) # water
        mc.setBlocks(x + 14, y - 3, z + 2, x + 12, y - 3, z + 2, 3) # dirt floor

        mc.setBlocks(x + 14, y - 1, z + 3, x + 11, y - 2, z + 3, 8) # water
        mc.setBlocks(x + 14, y - 3, z + 3, x + 12, y - 3, z + 3, 3) # dirt floor
        mc.setBlock(x + 14, y - 3, z + 3, 13) # gravel floor

        mc.setBlocks(x + 13, y - 1, z + 4, x + 11, y - 2, z + 4, 8) # water
        mc.setBlock(x + 13, y - 3, z + 4, 3) # dirt floor
        mc.setBlocks(x + 12, y - 3, z + 4, x + 11, y - 3, z + 4, 13) # gravel floor
        mc.setBlocks(x + 10, y - 1, z + 4, x + 10, y - 1, z + 5, 8) # water
        mc.setBlocks(x + 10, y - 2, z + 4, x + 10, y - 2, z + 5, 12) # sand floor

        mc.setBlocks(x + 13, y - 1, z + 5, x + 11, y - 2, z + 5, 8) # water
        mc.setBlocks(x + 13, y - 3, z + 5, x + 11, y - 3, z + 5, 13) #gravel floor

        mc.setBlocks(x + 13, y - 1, z + 6, x + 12, y - 2, z + 6, 8) # water
        mc.setBlocks(x + 13, y - 3, z + 6, x + 12, y - 3, z + 6, 13) # gravel floor
        for i in range(0, 4, 3):
            mc.setBlock(x + 11 + i, y - 1, z + 6, 8) # water
            mc.setBlock(x + 11 + i, y - 2, z + 6, 12) # sand floor
        
        mc.setBlocks(x + 13, y - 1, z + 7, x + 12, y - 1, z + 7, 8) # water
        mc.setBlocks(x + 13, y - 2, z + 7, x + 12, y - 2, z + 7, 12) # sand floor


        # lily pads
        mc.setBlock(x + 15, y, z + 1, 111)
        mc.setBlock(x + 13, y, z + 1, 111)
        mc.setBlock(x + 13, y, z + 3, 111)
        mc.setBlock(x + 12, y, z + 5, 111)
        mc.setBlock(x + 10, y, z + 5, 111)
        mc.setBlock(x + 13, y, z + 7, 111)


        # pond decorations

        # sea pickles
        for i in range(0, 3):
            mcr.command(f"setblock {x + 12} {y - 2} {z + 4} minecraft:sea_pickle")
            i += 1
        # kelp
        for i in range(0, 3, 2):
            for j in range (0, 1):
                mcr.command(f"setblock {x + 11 + i} {y - 2 + j} {z + 4} minecraft:kelp")
        for i in range(0, 3, 2):
            for j in range (0, 1):
                mcr.command(f"setblock {x + 12} {y - 2 + j} {z + 3 + i} minecraft:kelp")

        # sea grass
        for i in range(0, 1):
            mcr.command(f"setblock {x + 15 - i} {y - 1} {z} minecraft:seagrass")
        for i in range(0, 3):
            mcr.command(f"setblock {x + 16 - i} {y - 1} {z + 1} minecraft:seagrass")
        mcr.command(f"setblock {x + 15} {y - 1} {z + 2} minecraft:seagrass")
        for i in range(0, 1):
            for j in range (0, 1):
                mcr.command(f"setblock {x + 14 - i} {y - 2} {z + 2 + j} minecraft:seagrass")
        for i in range(0, 5, 4):
            mcr.command(f"setblock {x + 12} {y - 2} {z + 2 + i} minecraft:seagrass")
        for i in range(0, 1):
            mcr.command(f"setblock {x + 13} {y - 2} {z + 5 + i} minecraft:seagrass")
        mcr.command(f"setblock {x + 12} {y - 2} {z + 6} minecraft:seagrass")
        for i in range(0, 1):
            mcr.command(f"setblock {x + 10} {y - 1} {z + 5} minecraft:seagrass")
        for i in range(0, 5, 4):
            mcr.command(f"setblock {x + 11} {y - 1} {z + 6} minecraft:seagrass")
        for i in range(0, 1):
            mcr.command(f"setblock {x + 13} {y - 1} {z + 7} minecraft:seagrass")


    # trampoline
        mcr.command(f"setblock {x + 10} {y} {z - 1} minecraft:scaffolding")
        mc.postToChat(f"{x + 10} {y} {z - 1}")
        mcr.command(f"setblock {x + 10} {y} {z} minecraft:scaffolding")
        mcr.command(f"setblock {x + 11} {y} {z - 1} minecraft:scaffolding")
        mcr.command(f"setblock {x + 11} {y} {z} minecraft:scaffolding")

        # pond corner
        mc.setBlocks(x + 7, y, z + 8, x + 9, y, z + 5, 18)
        mc.setBlocks(x + 10, y, z + 8, x + 11, y, z + 7, 18)
        mc.setBlock(x + 12, y, z + 8, 18)
        mc.setBlock(x + 10, y, z + 6, 18)
        mc.setBlock(x + 8, y, z + 4, 18)
        mc.setBlocks(x + 8, y + 1, z + 5, x + 8, y + 1, z + 7, 18)
        mc.setBlock(x + 9, y + 1, z + 7, 18)
        mc.setBlocks(x + 9, y + 1, z + 8, x + 11, y + 1, z + 8, 18)

        # desert corner
        mc.setBlocks(x + 23, y, z + 8, x + 22, y + 1, z + 6, 18)
        mc.setBlock(x + 22, y + 1, z + 6, 0) # removes excess leaf block
        mc.setBlock(x + 23, y, z + 5, 18)
        mc.setBlocks(x + 21, y, z + 8, x + 21, y + 1, z + 7, 18)
        mc.setBlock(x + 21, y + 1, z + 7, 0) # removes excess leaf block
        mc.setBlock(x + 20, y, z + 8, 18)
        mc.setBlocks(x + 23, y + 2, z + 8, x + 22, y + 2, z + 7, 18)
        mc.setBlock(x + 22, y + 2, z + 7, 0) # removes excess leave block
        mc.setBlock(x + 23, y + 2, z + 8, 0) # removes excess leave block


        # trampoline
        mcr.command(f"setblock {x + 10} {y} {z - 1} minecraft:scaffolding")
        mcr.command(f"setblock {x + 10} {y} {z} minecraft:scaffolding")
        mcr.command(f"setblock {x + 11} {y} {z - 1} minecraft:scaffolding")
        mcr.command(f"setblock {x + 11} {y} {z} minecraft:scaffolding")

        
        # cacti/dead bushes
        mc.setBlocks(x + 16, y, z + 6, x + 16, y + 1, z + 6, 81) # pond-side
        mc.setBlocks(x + 22, y, z + 3, x + 22, y + 2, z + 3, 81) # armor-stand-side
        mc.setBlock(x + 15, y, z + 4, 32) # pond-side
        mc.setBlock(x + 18, y, z + 1, 32) # armor-stand-side

        # campfire
        mcr.command(f"setblock {x + 19} {y} {z + 4} minecraft:campfire")
        for i in range(0, 3, 2):
            mc.setBlock(x + 19, y, z + 5 - i, 44, 3)
        for i in range(0, 3, 2):
            mc.setBlock(x + 18 + i, y, z + 4, 44, 3)

        # armor stand
        mcr.command(f"setblock {x + 20} {y} {z + 1} minecraft:armor_stand")

        # flower fence
        for i in range(0, 3):
            mcr.command(f"setblock {x + 16 + i} {y} {z + 8} minecraft:oak_fence")
        mcr.command(f"setblock {x + 16} {y + 1} {z + 8} minecraft:potted_dandelion")
        mcr.command(f"setblock {x + 17} {y + 1} {z + 8} minecraft:potted_red_tulip")
        mcr.command(f"setblock {x + 18} {y + 1} {z + 8} minecraft:potted_blue_orchid")
        



    
    


    


    