from mcpi import minecraft
from mcrcon import MCRcon
from Structures import Structures

mcr = MCRcon("localhost", "123")
mcr.connect()


class Playground(Structures):
    
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 8, 8, 'Playground')
        
        
    
    def generatePlayground(self):
        mc = minecraft.Minecraft.create()
        
        x = self.x
        y = self.y
        z = self.z


        while mc.getBlock(x, y - 1, z) == 0:
            y -= 1


        mc.setBlocks(x + 8, y + 10, z + 8, x - 8, y, z - 8, 0) # space for playground building
        mc.setBlocks(x + 7, y - 1, z - 7, x - 7, y - 3, z + 7, 98) # floor under playground


        # playground foundation

        mc.setBlocks(x + 5, y, z + 5, x - 5, y - 2, z - 5, 12) # sand floor
        for i in range(0, 13, 12):
            # wood log perimeter
            mc.setBlocks(x + 6 - i, y, z + 6, x + 6 - i, y, z - 6, 17) 
            mc.setBlocks(x + 6, y, z + 6 - i, x - 6, y, z + 6 - i, 17)

            # leaves as hedge around playground
            mc.setBlocks(x + 6 - i, y + 1, z + 6, x + 6 - i, y + 5, z - 6, 18) 
            mc.setBlocks(x + 6, y + 1, z + 6 - i, x - 6, y + 5, z + 6 - i, 18)
        
        # removing corner of hedge to create entrance
        mc.setBlock(x + 6, y, z - 6, 0)
        for i in range(0, 5):
            mc.setBlocks(x + 6, y + 1 + i, z - 6, x + 3 - i, y + 1 + i, z - 3 + i, 0)
        

        # entrance to playground (wood planks)

        mc.setBlocks(x + 6, y, z - 4, x + 5, y, z - 3, 5)
        mc.setBlocks(x + 4, y, z - 6, x + 3, y, z - 5, 5)
        mc.setBlock(x + 4, y, z - 4, 5)
        mc.setBlocks(x + 6, y, z - 5, x + 5, y, z - 5, 53, 2) # north facing
        mc.setBlock(x + 5, y, z - 6, 53, 1) # east facing


        # sandbox
        mc.setBlocks(x, y, z - 5, x - 5, y, z - 5, 5, 5) # north wall
        mc.setBlocks(x - 5, y, z - 5, x - 5, y, z - 2, 5, 5) # west wall
        mc.setBlocks(x, y, z - 2, x - 4, y, z - 2, 126, 5) # south wall
        mc.setBlocks(x, y, z - 3, x, y, z - 4, 126, 5) # east wall
        mc.setBlocks(x - 1, y - 1, z - 3, x - 4, y - 1, z - 4, 0) # space



        # swing set

        # sides
        for i in range(0, 5, 4):
            mcr.command(f"setblock {x - 1 - i} {y + 1} {z} minecraft:oak_fence")
            mcr.command(f"setblock {x - 1 - i} {y + 1} {z + 4} minecraft:oak_fence")
            for j in range(0, 3, 2):
                for k in range(0, 3):
                    mcr.command(f"setblock {x - 2 - j} {y + 1 + k} {z + i} minecraft:oak_fence")
                    mcr.command(f"setblock {x - 3} {y + 3 + k} {z + i} minecraft:oak_fence")
        
        # swing hanger
        for i in range(0, 5):
            mcr.command(f"setblock {x - 3} {y + 6} {z + i} minecraft:dark_oak_slab")
        
        # swing chain
        for i in range(0, 3, 2):
            for j in range(0, 4):
                mcr.command(f"setblock {x - 3} {y + 2 + j} {z + 1 + i} minecraft:chain")
        
            # swing seat
            mcr.command(f"setblock {x - 3} {y + 1} {z + 1 + i} minecraft:dark_oak_slab[type= top]")
        mcr.command(f"setblock {x - 3} {y + 1} {z + 2} minecraft:dark_oak_slab")


        # slide

        # platform
        mc.setBlocks(x + 2, y + 4, z + 2, x + 4, y + 4, z + 4, 5)

        # pillars + fences above pillars
        for i in range(0, 3, 2):
            for j in range(0, 3, 2):
                mc.setBlocks(x + 2 + i, y + 1, z + 2 + j, x + 2 + i, y + 4, z + 2 + j, 17)
                for k in range(0, 3):
                    mcr.command(f"setblock {x + 2 + i} {y + 5 + k} {z + 2 + j} minecraft:oak_fence")
        
        # stairs + powered rails
        mc.setBlock(x + 3, y + 5, z + 2, 27) # powered rail start
        for i in range(0, 4):
            mc.setBlock(x + 3, y + 3 - i, z + 1 - i, 53, 7)
            mc.setBlock(x + 3, y + 4 - i, z + 1 - i, 27)

        # slide railing
        for i in range(0, 3, 2):
            mcr.command(f"setblock {x + 2 + i} {y + 5} {z + 3} minecraft:oak_fence")

        # platform roof
        mc.setBlocks(x + 2, y + 8, z + 2, x + 4, y + 8, z + 4, 126, 5)
        mc.setBlock(x + 3, y + 8, z + 3, 5, 5)
        

        # staircase to slide
        for j in range(0, 5, 4):
            mc.setBlock(x + 1 + j, y + 3, z + 5, 5) # corners
            for i in range(0, 3):
                mc.setBlock(x + 1 + j, y + 1 + i, z + 2 + i, 53, 2) # parallel stairs
        mc.setBlock(x + 2, y + 4, z + 5, 53) # top of stairs // west facing
        mc.setBlock(x + 4, y + 4, z + 5, 53, 1) # top of stairs // east facing
        mc.setBlock(x + 3, y + 4, z + 5, 5) # top of stairs center piece