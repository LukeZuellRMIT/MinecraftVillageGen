from mcpi import minecraft

mc = minecraft.Minecraft.create()

def curvedWall(xx, yy, zz, direction):

    a = xx
    b = yy
    c = zz

    while mc.getBlock(a, b , c) != 98:
        mc.setBlocks(a, b, c, a, b + 2, c, 98)
        if direction == 's':
            a -= 1
            c -= 1
        if direction == 'w':
            a -= 1
            c -= 1
        if direction == 'n':
            a += 1
            c += 1
        if direction == 'e':
            a -= 1
            c += 1
        

def generateFences(houseLength, houseWidth, x, y, z):
    
    # south
    mc.setBlocks(x + houseWidth + 3, y, z + houseLength + 9, x - houseWidth - 3, y + 2, z + houseLength + 9, 98)

    # west
    mc.setBlocks(x - houseWidth - 9, y, z - houseLength - 3, x - houseWidth - 9, y + 2, z + houseLength + 3, 98)

    # north
    mc.setBlocks(x - houseWidth - 3, y, z - houseLength - 9, x + houseWidth + 3, y + 2, z - houseLength - 9, 98)

    # east
    mc.setBlocks(x + houseWidth + 16, y, z + 5, x + houseWidth + 16, y + 2, z - 5, 98)
    

    # south curved wall
    xS, zS = x - houseWidth - 3, z + houseLength + 9
    curvedWall(xS, y, zS, 's')

    # west curved wall
    xW, zW = x - houseWidth - 9, z - houseLength - 3
    curvedWall(xW, y, zW, 'w')

    # north curved wall
    xN, zN = x + houseWidth + 3, z - houseLength - 9
    curvedWall(xN, y, zN, 'n')

    # east curved wall
    xE, zE = x + houseWidth + 16, z + 5
    curvedWall(xE, y, zE, 'e')


    