from asyncio import as_completed
from re import L
from statistics import mean
from mcpi import minecraft
import mcpi.block as block
import concurrent.futures 
import math
import time
import json

#A star code referenced from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
area_radius = 45

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    

class Path():
    def __init__(self, coordinates_to_connect):
        self.coordinates_to_connect = coordinates_to_connect
        self.coordinates_connected = []
        self.area_scan = []
        
    
    # areaScan functions scans an area return a dictionary in the format found below. This data is used for pathfinding algorithm.
    def areaScan(self, x, z):
        mc = minecraft.Minecraft.create()
            
        mc.postToChat('Path building has begun...')
        mc.postToChat('Scanning area...')     
           
        # Data will be store in this format:
        #       {  
        #            x1 : 
        #                {
        #                   z1 : [block_height 5, block_type: 2],
        #                   z2 : [block_height 3, block_type: 1],
        #                },
        #            x2 : 
        #                {
        #                   z1 : [block_height 5, block_type: 3],
        #                   z2 : [block_height 3, block_type: 1],
        #                },
        #       },
        # 
        
            
        vals = []
        
        
        for x_val in range(x - area_radius, x + area_radius):
            vals.append([x_val, z])
            
        start = time.time()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            results = executor.map(zScan, vals)
            
            data = {}
            
            for result in results:
                data[result['x_coordinate']] = result['z_data']
            
            out = json.dumps(data, indent=4)
            #print(out)
        
        self.area_scan = data
        end = time.time()
        timeString = f'scanning complete. It took:{end - start: .2f} seconds'
        mc.postToChat(timeString)
        
        
    def astar(self, origin, start, end): 
        start_timer = time.time()
        #takes in a start and end coord - Josh
        mc = minecraft.Minecraft.create()
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:
            lap_time = time.time()
            if (lap_time - start_timer > 5.00): 
                print("No path found, timeout")
                return
            # Get the current node
            current_node = open_list[0]
            
            #ensure that the current node is the one with the smallest cost in the open list -Josh
            for node in open_list:
                if node.f < current_node.f: #if there is another node found in the open list with a smaller f num, set it to current node -Josh
                    current_node = node

            # Pop current off open list, add to closed list
            open_list.remove(current_node)
            closed_list.append(current_node)
            
            # Found the goal node!
            if current_node == end_node:
                print("path found")
                path = []
                current = current_node
                mc.setBlocks(current.position[0] - 1, self.area_scan[current.position[0]][current.position[1]][0], current.position[1] + 1, current.position[0] + 1, self.area_scan[current.position[0]][current.position[1]][0], current.position[1] - 1, 4)
                while current is not None:
                    #place blocks down for the path -Josh
                    x = current.position[0]
                    y = self.area_scan[current.position[0]][current.position[1]][0]
                    try:
                        y_next = self.area_scan[current.parent.position[0]][current.parent.position[1]][0]
                    except:
                        y_next = y
                    try:
                        y_next_next = self.area_scan[current.parent.parent.position[0]][current.parent.parent.position[1]][0]
                    except:
                        y_next_next = y_next
                    try:
                        y_next_next_next = self.area_scan[current.parent.parent.parent.position[0]][current.parent.parent.parent.position[1]][0]
                    except:
                        y_next_next_next = y_next_next
                    z = current.position[1]
                    #clear the node position with air
                    mc.setBlocks(x - 1, y, z + 1, x + 1, y + 3, z - 1, 0)
                    #place down the blocks for the node,  using the average of the next 4 node heights for its own height. This creates a smoother and flatter path.
                    mc.setBlocks(x - 1, y - 5, z + 1, x + 1, mean([y, y_next, y_next_next, y_next_next_next]), z - 1, 4)
                    
                    
                    
                    
                    path.append(current.position)
                    last_node = current
                    current = current.parent
                #return path[::-1] # Return reversed path
                mc.setBlocks(last_node.position[0] - 1, self.area_scan[last_node.position[0]][last_node.position[1]][0], last_node.position[1] + 1, last_node.position[0] + 1, self.area_scan[last_node.position[0]][last_node.position[1]][0], last_node.position[1] - 1, 4)
                return

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
                
                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                
                # Make sure within range of the area_scan (at the moment it is a 40x40 around the player position) -Josh
                #check the node_position to see if it is in the domain of area_scan
                #use the parameter passed in called 'origin', this will be the players pos used to do the area_scan. 
                if (node_position[0] not in range(origin[0]-area_radius, origin[0]+area_radius)) or (node_position[1] not in range(origin[1]-area_radius, origin[1]+area_radius)):
                    continue

                # Make sure walkable terrain
                
                #check the height of the block: make sure that the height does not exceed -1 or +1 from the height of current node
                node_height = self.area_scan[node_position[0]][node_position[1]][0]
                current_height = self.area_scan[current_node.position[0]][current_node.position[1]][0]
                if (node_height > current_height + 1) or (node_height < current_height - 1):
                    continue
                
                #check that the block type is not water
                node_btype = self.area_scan[node_position[0]][node_position[1]][1]
                invalid_block_id = [8, 98, 3, 208]
                if node_btype in invalid_block_id:#water block type = 8
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                exists = False
                # Child is on the closed list
                for node in closed_list:
                    if node.position == child.position:
                        #print("ALREADY IN CLOSED LIST")
                        exists = True
                        break
                if exists == True: continue

                # Create the f, g, and h values using pythag but without squaring
                child.g = current_node.g + 1
                child.h = math.floor(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child.position == open_node.position and child.g > open_node.g:
                        #print("ALREADY IN OPEN LIST")
                        exists = True
                        break
                if exists == True: continue

                # Add the child to the open list
                open_list.append(child)
            
        
def zScan(vals):
    mc = minecraft.Minecraft.create()
    # This will scan each block in a given y range
    
    x = vals[0]
    z = vals[1]
    
    
    
    z_data = {}
    
    for z_val in range(z - area_radius , z + area_radius):
        
        height = mc.getHeight(x, z_val)
        blockID = mc.getBlock(x, height, z_val)
        z_values = []
        
        
        z_values.append(height)
        z_values.append(blockID)
        z_data[z_val] = z_values
        
    
    outputDict = {}
    
    outputDict['x_coordinate'] = x
    outputDict['z_data'] = z_data
    
    
    return outputDict

def generatePath(doorPoints, x, z):
    mc = minecraft.Minecraft.create()
    path = Path(5)

    path.areaScan(x, z)
    print(doorPoints)
    
    for i in range(0,len(doorPoints)-1):
        start = doorPoints[i]
        end = doorPoints[i+1]
        print(f'creating path from {start} ---> {end}')
        path.astar((x, z),start, end)

    
