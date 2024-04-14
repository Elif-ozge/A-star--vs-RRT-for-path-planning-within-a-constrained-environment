import queue
from sensory import *
from AdjList import *
from Environment import *
import time

class Astar:
    
    def __init__(self,env):
        self.que=queue.PriorityQueue()
        self.cost=0
        self.curr_env=env
        self.start=env.start_state
        self.goal=env.goal_state #tuple
        self.expanded=[]
        self.visited=[]
        self.edges=[]
    
    def heuristic(self,node):
        goal_distance=( (node.x-self.goal[0])**2 + (node.y-self.goal[1])**2)**(0.5)
        val=node.cost+goal_distance
        return val
    
    def contains(self, cell):
        arr=[]
        bool=False
        while not self.que.empty():
            curr=self.que.get()
            arr.append(curr)
            if curr.nodeCode == cell.nodeCode:
                bool= True
        
        for cell in arr:
            self.que.put(cell)
            
        return bool    
    def Astar_Alg(self):

        sensor= Sensory(grid_size,grid_size)
        # boolean checks for whether its a goal state or its not possible to park specified area
        run=True
        start_nod=None
        self.start_time = time.time()

        # initialize start node
        for cell in gridcells.ADJList:
            if cell.x==self.start[0]+grid_size/2 and cell.y==self.start[1]+grid_size/2:
                start_nod=cell
        if start_nod==None:
            print("could not find start nod!")
            return
       
        start_nod.heuristic=float('inf')
        start_nod.parent=None
        start_nod.cost=0
        self.que.put(start_nod)
        self.curr_env.adjlist.addNode(start_nod)          
        curr_nod=start_nod
        prev_nod=None
        curr_x=0
        curr_y=0

        
        while not self.que.empty():
            
            curr_nod=self.que.get()
            
            
            # Check if maximum time limit exceeded
            if time.time() - self.start_time > 5:
                print("Time limit exceeded. Terminating Astar algorithm.")
                print("Goal not found")
                return
            
            
            # update current coordinates and percept range
            curr_x=curr_nod.x
            curr_y=curr_nod.y
            max_x=min(width,curr_x+sensor.width)
            max_y=min(height,curr_y+sensor.height)
            min_x=max(0,curr_x-sensor.width)
            min_y=max(0,curr_y-sensor.height)
            
                 #check goal state
            if ( curr_nod!=None and curr_nod.x==self.goal[0])  and curr_nod.y==self.goal[1] :  
                    print("goal found!")
                    timex=time.time()
                    #print(curr_nod.parent)
                    time.sleep(0.1)
                    self.draw_path(curr_nod,(250,0,110),70)
                    time.sleep(0.1)
                    path=self.curr_env.find_path(start_nod,curr_nod,(100,0,0),3)
                    self.curr_env.move_car_along_path(path,speed=1)
                    return timex-self.start_time
            
            for cell in gridcells.ADJList[int(curr_nod.nodeCode)].adjacencies:
                if min_x <= cell.x <= max_x and min_y <= cell.y <= max_y:                        
                        if gridcells.ADJList[int(cell.nodeCode)].color != 'Blue' and  gridcells.ADJList[int(cell.nodeCode)].color!='White':
                           # if  prev_nod!=None and self.curr_env.is_clear_path(prev_nod,curr_nod):
                                if   not self.contains(cell)  and not self.expanded.__contains__(cell.nodeCode):
                                    cell.cost=( (cell.x-self.start[0])**2 + (cell.y-self.start[1])**2)**(0.5)
                                    cell.heuristic=self.heuristic(cell) 
                                    self.visited.append(cell.nodeCode)
                                    self.curr_env.adjlist.addNode(cell)
                                    print("cell: " ,cell.nodeCode)
                                    time.sleep(0.01)
                                    if self.curr_env.is_clear_pathA_star(curr_nod,cell):
                                        j=random.uniform(0,1)
                                        if cell.heuristic < curr_nod.heuristic :
                                                self.curr_env.adjlist.addEdge(curr_nod,cell)
                                                self.que.put(cell)
                                                self.edges.append((cell,curr_nod)) 
                                                #print(cell.nodeCode, curr_nod.nodeCode)
                                        elif j>0.5:
                                                self.curr_env.adjlist.addEdge(curr_nod,cell)
                                                self.que.put(cell)
                                                self.edges.append((cell,curr_nod)) 
                                                #print(cell.nodeCode, curr_nod.nodeCode)
                                            
                                       
                #self.draw_edges()   # if you want to see the edges algorithm traverses to find the path 
                                        # uncomment it c:  
                pygame.display.update()
                
            self.expanded.append(curr_nod.nodeCode)
           

        print("queue empty. No solution found!")
      
    def draw_edges(self):
        for i, edge in enumerate(self.edges):
            # Decrease red component gradually, ensuring it stays within the valid range
            red_component = max(0, 255 - i % 256)
            color = (red_component, 192, 203)
            pygame.draw.line(self.curr_env.board, color, (edge[0].x, edge[0].y), (edge[1].x, edge[1].y), 2)

    def draw_path(self, goal_nod,path_color, alpha):
        # Start from the goal node
        curr_node = goal_nod
        
        #print(goal_nod.parent)
        # Traverse back to the start node
        while curr_node.parent is not None:
            print('iiii',curr_node.parent.nodeCode)
            # Create a surface with the specified color
            surface = pygame.Surface((grid_size, grid_size))
            surface.fill(path_color)
            # Set the alpha value for transparency
            surface.set_alpha(alpha)
            # Draw the surface onto the environment board
            self.curr_env.board.blit(surface, (curr_node.x - grid_size/2, curr_node.y - grid_size/2))
            curr_node = curr_node.parent