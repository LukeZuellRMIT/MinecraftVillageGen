import concurrent.futures
from mcpi import minecraft

# areaScan creates multiple threads for each x value that requires scanning.
# Returns a list of height values which is then used to select what height the house should be placed.
def areaScan(x, z, width, length):
    
    vals = []
    
    for x_val in range(x - width, x + width):
        vals.append([x_val, z, length]) 
    
    height_vals = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        
        results = executor.map(zScan, vals)
        
        for result in results:
            for each in result:
                height_vals.append(each)
                
    return height_vals
        
            
# zScans runs in the positive and negative z directions placing 
# an air block each time it encounters a block in the bad blocks list.
def zScan(vals):
    mc = minecraft.Minecraft.create()
    
    x = vals[0]
    z = vals[1]
    length = vals[2]
    
    heights = []
    bad_blocks = [0, 175, 18, 161, 17, 162, 99, 100, 31]
    
    for z_val in range(z - length , z + length):
        
        block_height  = mc.getHeight(x, z_val)
        block_type = mc.getBlock(x, block_height, z_val) 
           
        while block_type in bad_blocks:
            mc.setBlock(x, block_height, z_val, 0)
            block_height  = mc.getHeight(x, z_val)
            block_type = mc.getBlock(x, block_height, z_val)
        
        heights.append(mc.getHeight(x, z_val))
        
    return heights