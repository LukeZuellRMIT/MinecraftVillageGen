from mcpi import minecraft
from mcrcon import MCRcon
from Structures import Structures

mcr = MCRcon("localhost", "123")
mcr.connect()


class Well(Structures):
    
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 9, 9, 'Well')
        
        
    
    def generateWell(self):
        mc = minecraft.Minecraft.create()
        
        x = self.x
        y = self.y
        z = self.z


        while mc.getBlock(x, y - 1, z) == 0:
            y -= 1

        
        # space for well building
        mc.setBlocks(x + 8, y + 12, z + 8, x - 8, y, z - 8, 0) 
        
        # floor under well
        mc.setBlocks(x + 8, y - 1, z - 8, x - 8, y - 3, z + 8, 98)
        
        # space for water in well
        mc.setBlocks(x + 1, y, z + 1, x - 1, y - 5, z - 1, 0) 
        
        for i in range(0, 5, 4):
            # inner walls of well
            mc.setBlocks(x + 2, y + 2, z - 2 + i, x - 2, y - 5, z - 2 + i, 98, 1)
            mc.setBlocks(x + 2 - i, y + 2, z + 2, x + 2 - i, y - 5, z - 2, 98, 1)
            
            # slabs for perimeter of well
            mc.setBlocks(x + 2, y + 3, z - 2 + i, x - 2, y + 3, z - 2 + i, 44, 5)
            mc.setBlocks(x + 2 - i, y + 3, z + 2, x + 2 - i, y + 3, z - 2, 44, 5)
            
            # pillars
            mc.setBlock(x + 2, y + 3, z - 2 + i, 98, 1)
            mc.setBlock(x - 2, y + 3, z + 2, 98, 1)
            mc.setBlock(x - 2, y + 3, z - 2, 98, 1)
            mcr.command(f"setblock {x + 2} {y + 4} {z - 2 + i} minecraft:mossy_stone_brick_wall")
            mcr.command(f"setblock {x - 2} {y + 4} {z - 2 + i} minecraft:mossy_stone_brick_wall")
            mc.setBlocks(x + 2, y + 5, z - 2 + i, x + 2, y + 6, z - 2 + i, 188)
            mc.setBlocks(x - 2, y + 5, z - 2 + i, x - 2, y + 6, z - 2 + i, 188)
            
            # roof foundation
            mc.setBlocks(x + 2, y + 7, z - 2 + i, x - 2, y + 7, z - 2 + i, 98, 1)
            mc.setBlocks(x + 2 - i, y + 7, z + 2, x + 2 - i, y + 7, z - 2, 98, 1)
            
            # lantern on ceiling
            mcr.command(f"setblock {x + 2 - i} {y + 6} {z} minecraft:lantern[hanging= true]")
            mcr.command(f"setblock {x} {y + 6} {z - 2 + i} minecraft:lantern[hanging= true]")
            
        # bottom of well
        mc.setBlocks(x + 1, y - 5, z + 1, x - 1, y - 5, z - 1, 98, 1) 
        
        # water
        mc.setBlocks(x + 1, y + 1, z + 1, x - 1, y - 4, z - 1, 8) 

        for i in range(0, 7, 6):
            # extension of well platform
            mc.setBlocks(x + 3, y + 2, z - 3 + i, x - 3, y, z - 3 + i, 98, 1)
            mc.setBlocks(x + 3 - i, y + 2, z + 3, x + 3 - i, y, z - 3, 98, 1)
            
            # wall around well
            for k in range(0, 6):
                mcr.command(f"setblock {x + 3 - k} {y + 3} {z - 3 + i} minecraft:stone_brick_wall")
                mcr.command(f"setblock {x + 3 - i} {y + 3} {z + 3 - k} minecraft:stone_brick_wall")
            
            mcr.command(f"setblock {x + 3} {y + 4} {z - 3 + i} minecraft:lantern")
            mcr.command(f"setblock {x - 3} {y + 4} {z - 3 + i} minecraft:lantern")
            mc.setBlock(x, y + 3, z - 3 + i, 183)
            mc.setBlock(x + 3 - i, y + 3, z, 183, 1)
        
        mcr.command(f"setblock {x - 3} {y + 3} {z - 3} minecraft:stone_brick_wall")

        # stairs
        
        for i in range(0, 3):
            #rails
            mc.setBlocks(x + 2, y - 1, z - 4, x - 2, y - 1, z - 7, 98)
            mc.setBlocks(x + 2, y + 1 - i, z - 4 - i, x - 2, y + 1 - i, z - 4 - i, 98)
            
            mc.setBlocks(x + 4, y - 1, z + 2, x + 7, y - 1, z - 2, 98)
            mc.setBlocks(x + 4 + i, y + 1 - i, z + 2, x + 4 + i, y + 1 - i, z - 2, 98)

            mc.setBlocks(x + 2, y - 1, z + 4, x - 2, y - 1, z + 7, 98)
            mc.setBlocks(x + 2, y + 1 - i, z + 4 + i, x - 2, y + 1 - i, z + 4 + i, 98)

            mc.setBlocks(x - 4, y - 1, z + 2, x - 7, y - 1, z - 2, 98)
            mc.setBlocks(x - 4 - i, y + 1 - i, z + 2, x - 4 - i, y + 1 - i, z - 2, 98)

            for k in range(0, 2):
                for j in range(0, 5, 4):
                    mcr.command(f"setblock {x + 2 - j} {y + 3 - i - k} {z - 4 - i} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x + 4 + i} {y + 3 - i - k} {z + 2 - j} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x + 2 - j} {y + 3 - i - k} {z + 4 + i} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x - 4 - i} {y + 3 - i - k} {z + 2 - j} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x + 2 - j} {y} {z - 7} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x + 7} {y} {z + 2 - j} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x + 2 - j} {y} {z + 7} minecraft:stone_brick_wall")
                    mcr.command(f"setblock {x - 7} {y} {z + 2 - j} minecraft:stone_brick_wall")
            
            

            
            # stairway
            mc.setBlocks(x + 1, y + 2 - i, z - 4 - i, x - 1, y + 2 - i, z - 4 - i, 109, 2)
            mc.setBlocks(x, y + 2 - i, z - 4 - i, x, y + 2 - i, z - 4 - i, 134, 2) # north facing

            mc.setBlocks(x + 4 + i, y + 2 - i, z + 1, x + 4 + i, y + 2 - i, z - 1, 109, 1)
            mc.setBlocks(x + 4 + i, y + 2 - i, z, x + 4 + i, y + 2 - i, z, 134, 1) # east facing

            mc.setBlocks(x + 1, y + 2 - i, z + 4 + i, x - 1, y + 2 - i, z + 4 + i, 109, 3)
            mc.setBlocks(x, y + 2 - i, z + 4 + i, x, y + 2 - i, z + 4 + i, 134, 3) # south facing

            mc.setBlocks(x - 4 - i, y + 2 - i, z + 1, x - 4 - i, y + 2 - i, z - 1, 109)
            mc.setBlocks(x - 4 - i, y + 2 - i, z, x - 4 - i, y + 2 - i, z, 134) # west facing


        # leaves
        for i in range(0, 2):
            mc.setBlocks(x - 4 + i, y + 3, z - 3 - i, x - 4 + i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x + 4 - i, y + 3, z + 3 + i, x + 4 - i, y, z + 3 + i, 18, 1)
            mc.setBlocks(x + 4 - i, y + 3, z - 3 - i, x + 4 - i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x - 4 + i, y + 3, z + 3 + i, x - 4 + i, y, z + 3 + i, 18, 1)
        for i in range(0, 3):
            mc.setBlocks(x - 5 + i, y + 2, z - 3 - i, x - 5 + i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x + 5 - i, y + 2, z + 3 + i, x + 5 - i, y, z + 3 + i, 18, 1)
            mc.setBlocks(x + 5 - i, y + 2, z - 3 - i, x + 5 - i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x - 5 + i, y + 2, z + 3 + i, x - 5 + i, y, z + 3 + i, 18, 1)
        for i in range(0, 4):
            mc.setBlocks(x - 6 + i, y + 1, z - 3 - i, x - 6 + i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x + 6 - i, y + 1, z + 3 + i, x + 6 - i, y, z + 3 + i, 18, 1)
            mc.setBlocks(x + 6 - i, y + 1, z - 3 - i, x + 6 - i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x - 6 + i, y + 1, z + 3 + i, x - 6 + i, y, z + 3 + i, 18, 1)
        for i in range(0, 5):
            mc.setBlocks(x - 7 + i, y, z - 3 - i, x - 7 + i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x + 7 - i, y, z + 3 + i, x + 7 - i, y, z + 3 + i, 18, 1)
            mc.setBlocks(x + 7 - i, y, z - 3 - i, x + 7 - i, y, z - 3 - i, 18, 1)
            mc.setBlocks(x - 7 + i, y, z + 3 + i, x - 7 + i, y, z + 3 + i, 18, 1)


        # roof
        mc.setBlock(x, y + 8, z, 98, 3) # center

        for i in range(0, 3, 2):

            # leaves above cross
            for k in range(0, 3, 2):
                mc.setBlock(x + 1 - i, y + 8 + k, z, 18, 1)
                mc.setBlock(x, y + 8 + k, z + 1 - i, 18, 1)

            # wood slab corners to center
            mcr.command(f"setblock {x + 1 - i} {y + 8} {z + 1} minecraft:spruce_slab[type= top]")
            mcr.command(f"setblock {x + 1 - i} {y + 8} {z - 1} minecraft:spruce_slab[type= top]")
        
        for i in range(0, 4):
            mcr.command(f"setblock {x} {y + 7 - i} {z} minecraft:chain")
        mcr.command(f"setblock {x} {y + 3} {z} minecraft:cauldron[level= 1]")

        for i in range(0, 3):
            mcr.command(f"setblock {x - 1} {y + 7 - i} {z} minecraft:chain")

        
        # stairs around roof
        mc.setBlocks(x + 2, y + 7, z - 3, x - 2, y + 7, z - 3, 109, 6) # north facing
        mc.setBlocks(x + 2, y + 7, z + 3, x - 2, y + 7, z + 3, 109, 7) # south facing
        mc.setBlocks(x + 3, y + 7, z + 2, x + 3, y + 7, z - 2, 109, 5) # east facing
        mc.setBlocks(x - 3, y + 7, z + 2, x - 3, y + 7, z - 2, 109, 4) # west facing
        for i in range(0, 7, 6):
            mc.setBlock(x + 3, y + 7, z + 3 - i, 109, 5) # east facing corners
            mc.setBlock(x - 3, y + 7, z + 3 - i, 109, 4) # west facing corners
        

        for i in range(0, 7, 6):
            # wood slab on corner
            mc.setBlock(x - 3, y + 8, z + 3 - i, 126, 1)
            mc.setBlock(x + 3, y + 8, z + 3 - i, 126, 1)
            mc.setBlock(x + 3 - i, y + 8, z + 3, 126, 1)
            mc.setBlock(x + 3 - i, y + 8, z - 3, 126, 1)
            
            # leaves on roof corners
            mc.setBlock(x + 2, y + 8, z + 3 - i, 18, 1)
            mc.setBlock(x - 2, y + 8, z + 3 - i, 18, 1)
            mc.setBlock(x + 3 - i, y + 8, z + 2, 18, 1)
            mc.setBlock(x + 3 - i, y + 8, z - 2, 18, 1)
            
            # wood planks next to outer center pieces
            mc.setBlocks(x + 3 - i, y + 8, z + 1, x + 3 - i, y + 8, z - 1, 5, 1)
            mc.setBlocks(x + 1, y + 8, z + 3 - i, x - 1, y + 8, z + 3 - i, 5, 1)
        
            # outer center pieces
            mc.setBlock(x + 3 - i, y + 8, z, 98, 3)
            mc.setBlock(x, y + 8, z + 3 - i, 98, 3)

            # slab on top of outer center pieces
            mc.setBlocks(x - 1, y + 9, z + 3 - i, x + 1, y + 9, z + 3 - i, 44, 5)
            mc.setBlocks(x + 3 - i, y + 9, z - 1, x + 3 - i, y + 9, z + 1, 44, 5)

        
        # emerald pyramid for beacon
        mc.setBlocks(x + 1, y + 9, z + 1, x - 1, y + 9, z - 1, 133) 

        # beacon
        mc.setBlock(x, y + 10, z, 138)

        
        for i in range(0, 3, 2):
            
            # planks around beacon
            mc.setBlock(x + 1 - i, y + 10, z + 1, 5, 1)
            mc.setBlock(x + 1 - i, y + 10, z - 1, 5, 1)

            # slabs around beacon
            mc.setBlock(x + 1 - i, y + 11, z + 1, 44, 5)
            mc.setBlock(x + 1 - i, y + 11, z - 1, 44, 5)
        
        # stone brick behind outer center pieces
        for i in range(0, 5, 4):
            mc.setBlock(x, y + 8, z + 2 - i, 98, 1)
            mc.setBlock(x + 2 - i, y + 8, z, 98, 1)

        # top roof corner
        mc.setBlock(x + 2, y + 10, z - 2, 109, 2)
        mc.setBlock(x - 2, y + 10, z - 2, 109, 2)
        mc.setBlock(x + 2, y + 10, z + 2, 109, 3)
        mc.setBlock(x - 2, y + 10, z + 2, 109, 3)

        # top roof sides
        mc.setBlocks(x + 1, y + 10, z - 2, x - 1, y + 10, z - 2, 134, 2) # north facing
        mc.setBlocks(x + 2, y + 10, z + 1, x + 2, y + 10, z - 1, 134, 1) # east facing
        mc.setBlocks(x + 1, y + 10, z + 2, x - 1, y + 10, z + 2, 134, 3) # south facing
        mc.setBlocks(x - 2, y + 10, z + 1, x - 2, y + 10, z - 1, 134) # west facing

        # stair above mossy stone brick
        mc.setBlock(x, y + 9, z + 2, 109, 3) # south
        mc.setBlock(x, y + 10, z + 2, 109, 7)
        mc.setBlock(x, y + 9, z - 2, 109, 2) # north
        mc.setBlock(x, y + 10, z - 2, 109, 6)
        mc.setBlock(x + 2, y + 9, z, 109, 1) # east
        mc.setBlock(x + 2, y + 10, z, 109, 5)
        mc.setBlock(x - 2, y + 9, z, 109) # west
        mc.setBlock(x - 2, y + 10, z, 109, 4)

        # stairs to the side of mossy stone brick
        
        for i in range(0, 5, 4):
            # stairs to the side of mossy stone brick
            mc.setBlock(x + 2 - i, y + 8, z - 1, 134, 2) # north
            mc.setBlock(x + 2 - i, y + 9, z - 1, 134, 6)
            mc.setBlock(x + 2 - i, y + 8, z + 1, 134, 3) # south
            mc.setBlock(x + 2 - i, y + 9, z + 1, 134, 7)
            mc.setBlock(x + 1, y + 8, z + 2 - i, 134, 1) # east
            mc.setBlock(x + 1, y + 9, z + 2 - i, 134, 5)
            mc.setBlock(x - 1, y + 8, z + 2 - i, 134) # east
            mc.setBlock(x - 1, y + 9, z + 2 - i, 134, 4)

            # slab on inner corner
            mc.setBlock(x + 2 - i, y + 8, z + 2, 126, 1)
            mc.setBlock(x + 2 - i, y + 8, z - 2, 126, 1)

            # lantern on corners
            mcr.command(f"setblock {x + 2 - i} {y + 9} {z + 2} minecraft:lantern[hanging= true]")
            mcr.command(f"setblock {x + 2 - i} {y + 9} {z - 2} minecraft:lantern[hanging= true]")