import random
from Environment import *
from sensory import *
import time

class RRT:
    
    def __init__(self,env):
        self.cost=0
        self.curr_env=env
        self.start=env.start_state
        self.goal=env.goal_state #tuple
        self.visited=[]
        self.edges=[]
        self.sensor= Sensory(grid_size*3,grid_size*3)
        self.start_time=0
        
        
    def rand_config(self,x_min, x_max, y_min, y_max):
        
        
        current_x = random.uniform(x_min, x_max)
        current_y = random.uniform(y_min, y_max)
        distance_to_goal = ((current_x - self.goal[0]) ** 2 + (current_y - self.goal[1]) ** 2) ** 0.5
        
        # Calculate the maximum distance within the bounds
        max_distance = max(x_max - x_min, y_max - y_min)
        
        # Calculate the bias factor based on the ratio of current distance to maximum distance
        bias_factor = 1.0 - (distance_to_goal / max_distance)
        
        # Apply bias to the random selection
        if random.random() < bias_factor:
            x = self.goal[0]
            y = self.goal[1]
        else:
            x = current_x
            y = current_y
            
        return (x, y)
        
    def nearest_vertex(self, qrand, current_node):
        nearest_vertex = None
        min_distance = float('inf')
        for cell in gridcells.ADJList:
            if cell == current_node:
                continue  # Skip the current node
            dist = ((cell.x - qrand[0])**2 + (cell.y - qrand[1])**2)**0.5  # qrand is a (x, y) tuple
            if dist < min_distance:
                nearest_vertex = cell
                min_distance = dist
            
        return nearest_vertex


    def RRT_Alg(self):

        start_nod=None
        
        # initialize start node
        for cell in gridcells.ADJList:
            if cell.x==self.start[0]+grid_size/2 and cell.y==self.start[1]+grid_size/2:
                start_nod=cell
        if start_nod==None:
            print("could not find start nod!")
            return
        
        start_nod.parent=None
        start_nod.cost=0
        self.curr_env.adjlist.addNode(start_nod)
        curr_nod=start_nod
        curr_x=0
        curr_y=0
        
        self.start_time = time.time()
        
        while True:
            
            # Check if maximum time limit exceeded
            if time.time() - self.start_time > 5:
                print("Time limit exceeded. Terminating RTT algorithm.")
                print("Goal not found")
                return
            
             #check goal state
            if curr_nod!=None and curr_nod.color=='Green':  
                print("goal found!")
                timex=time.time()
                time.sleep(0.1)
                path=self.curr_env.find_path(start_nod,nearest_cell,(100,0,0),3)
                time.sleep(0.01)
                self.curr_env.move_car_along_path(path,speed=1)
                return timex-self.start_time
                
            # update current coordinates and percept range
            curr_x=curr_nod.x
            curr_y=curr_nod.y
            max_x=min(width,curr_x+self.sensor.width)
            max_y=min(height,curr_y+self.sensor.height)
            min_x=max(0,curr_x-self.sensor.width)
            min_y=max(0,curr_y-self.sensor.height)
            
            config_curr=self.rand_config(min_x,max_x,min_y,max_y)
            nearest_cell=self.nearest_vertex(config_curr,curr_nod)
            
            if gridcells.ADJList[int(nearest_cell.nodeCode)].color != 'Blue' and  gridcells.ADJList[int(nearest_cell.nodeCode)].color!='White': # if its not an obstacle or a parking line    
                if self.curr_env.is_clear_pathRRT(curr_nod,nearest_cell):    
                    if nearest_cell.nodeCode not in self.visited:
                        self.curr_env.adjlist.addNode(nearest_cell)
                        self.curr_env.adjlist.addEdge(curr_nod,nearest_cell)
                        self.visited.append(curr_nod.nodeCode)
                        self.edges.append((curr_nod,nearest_cell))

                    curr_nod=nearest_cell 

                
                #self.curr_env.drawEdges(self.edges)   # if you want to see the edges algorithm traverses to find the path 
                                                             # uncomment it c:
                pygame.display.update()         
                 

            
                    

                

        
        

