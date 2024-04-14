import pygame
import math,random
from AdjList import *
import time

#board constants
width = 1000
height = 800
radius = 20
grid_size=40
max_nodes = 5000
car_length = grid_size*2
car_width = grid_size*2
parking_lot_width = math.ceil(((car_width + 20 )/grid_size))*grid_size
parking_lot_height =  math.ceil(((car_length + 20) /grid_size))*grid_size
parking_line_Width= grid_size
gridcells=ADJLIST()
path_points=[]

## vparking lota bak sonra
class ParkingLot:
    
    def __init__(self,topleft_x,topleft_y,width,height,full,isGoal):
        self.x=topleft_x+grid_size
        self.y=topleft_y
        self.full=full
        self.isgoal=isGoal
        self.width=width
        self.height=height
        
class Obstacles:
    def __init__(self,x,y,w,h) :
        self.x=x
        self.y=y
        self.width=w
        self.height=h

class GridCells:
    def __init__(self,centerx,centery,gridNo,color):
        self.x=centerx
        self.y=centery
        self.GridNum=gridNo
        self.color=color
    
class Car:
    
    def __init__(self):
        self.centerx=(car_length/2)
        self.centery= ((height/grid_size)/2)*grid_size
        
    def update_x(self,x):
        self.centerx=x
        
    def update_y(self,y):
        self.centery=y
    
    def getx(self):
        return self.centerx
    
    def gety(self):
        return self.centery

class Environment :
    
                            
    def __init__(self, NumLots, technique = 0 ) :
        
        self.num_of_parking_lots=NumLots
        self.parking_technique=technique
        self.lots=[]  # an array that holds ParkingLot objects 
        self.obstacles=[]
        self.adjlist=ADJLIST() ## to save paths ad nodes explored while applying algorithms
        self.goal_state=None
        self.start_state=None
        
        #initialize board
        pygame.init()
        self.board = pygame.display.set_mode((width,height))
        self.board.fill((0,0,0))
        pygame.display.set_caption('Self-Parking Agent')
        
        #initialize car
        self.car=Car()
        pygame.draw.rect(self.board,(250,0,110),(0,self.car.centery,car_length,car_width))
        self.start_state=(40,400)
        self.initialize_gridcells()
        
        length=0
        while length < car_length:
            index1 = int(((self.car.centery+grid_size)/grid_size)*(width/grid_size) + int(length/grid_size))
            index2 = int(((self.car.centery)/grid_size)*(width/grid_size) + int(length/grid_size))
            if 0 <= index1 < (gridcells.nodeCount):
                gridcells.ADJList[index1].color = "Pink"
            if 0 <= index2 < (gridcells.nodeCount):
                gridcells.ADJList[index2].color = "Pink"
            length += grid_size
            
        self.draw_gridcells()
        

    
        #for x in range(0, width, grid_size):
          #  pygame.draw.line(self.board, (100, 100, 100), (x, 0), (x, height))
        #for y in range(0, height, grid_size):
         #   pygame.draw.line(self.board, (100, 100, 100), (0, y), (width, y))
            
        #car_image = pygame.image.load("carimg.jpg")
        #self.board.blit(car_image, (start_x, start_y))
        
    ## environment instances from easy to hard 
     ## they also initialize "lots" array at line 29
    
    def draw_gridcells(self):
        for cell in gridcells.ADJList:
            pygame.draw.line(self.board, (100, 100, 100), (cell.x-grid_size/2 , 0), (cell.x-grid_size/2, height))
            pygame.draw.line(self.board, (100, 100, 100), (0,cell.y-grid_size/2), (width, cell.y-grid_size/2))
            pygame.draw.circle(self.board,(200,200,200),width=5, center=(cell.x,cell.y),radius=4)
            
            '''
            # this part used to help debugging please do not uncomment it if not necessary
            font = pygame.font.Font(None, 20)
            text_surface = font.render(str(cell.nodeCode), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(cell.x, cell.y))
            self.board.blit(text_surface, text_rect)
            '''
            
            
    def initialize_gridcells(self):
        prev=None
        for y in range(0,int(height/grid_size)):
            for x in range(0,int(width/grid_size)):
                curr_nod=MyNode((x+0.5)*grid_size,(y+0.5)*grid_size,None,y*(width/grid_size)+x,"Black")
                if curr_nod.x + grid_size < width:
                    curr_nod.adjacencies.append(MyNode((x+1.5)*grid_size,(y+0.5)*grid_size,None,y*(width/grid_size)+x+1,"Black"))
                    
                if curr_nod.x-grid_size > 0:
                    curr_nod.adjacencies.append(MyNode((x-0.5)*grid_size,(y+0.5)*grid_size,None,y*(width/grid_size)+x-1,"Black"))
                    
                if curr_nod.y-grid_size > 0:
                    curr_nod.adjacencies.append(MyNode((x+0.5)*grid_size,(y-0.5)*grid_size,None,(y-1)*(width/grid_size)+x,"Black"))
                    
                if curr_nod.y+grid_size < height:
                    curr_nod.adjacencies.append(MyNode((x+0.5)*grid_size,(y+1.5)*grid_size,None,(y+1)*(width/grid_size)+x,"Black"))
                
                
                # Add diagonal neighbors
                if curr_nod.x + grid_size < width and curr_nod.y - grid_size > 0:
                    curr_nod.adjacencies.append(MyNode((x+1.5)*grid_size, (y-0.5)*grid_size, None, (y-1)*(width/grid_size)+x+1, "Black"))
                    
                if curr_nod.x + grid_size < width and curr_nod.y + grid_size < height:
                    curr_nod.adjacencies.append(MyNode((x+1.5)*grid_size, (y+1.5)*grid_size, None, (y+1)*(width/grid_size)+x+1, "Black"))
                    
                if curr_nod.x - grid_size > 0 and curr_nod.y - grid_size > 0:
                    curr_nod.adjacencies.append(MyNode((x-0.5)*grid_size, (y-0.5)*grid_size, None, (y-1)*(width/grid_size)+x-1, "Black"))
                    
                if curr_nod.x - grid_size > 0 and curr_nod.y + grid_size < height:
                    curr_nod.adjacencies.append(MyNode((x-0.5)*grid_size, (y+1.5)*grid_size, None, (y+1)*(width/grid_size)+x-1, "Black"))
                    
                gridcells.addNode(curr_nod)
                prev=curr_nod
       
        return        
    
    
    
    def env0(self):
        
        starting_x_u=-1
        starting_y_u=0
        line=0 
        col=0 
        starting_x_d=-1
        counter=0

        #vertical park
        if(self.parking_technique==0):
            
            end_y=height-parking_lot_height
            
            while starting_y_u < parking_lot_height:
                starting_x_u=0
                starting_x_d=0
                while starting_x_u<(width) and starting_x_d<(width):
                    pygame.display.update()
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_u,starting_y_u,grid_size,grid_size))
                   # print(".........")
                    #print(starting_x_u)
                    if starting_x_u +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_u,0,parking_lot_width,parking_lot_height,0,False))
                    line=int(starting_y_u/grid_size)
                    col=int(starting_x_u/grid_size)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_u+= parking_lot_width + parking_line_Width
                    #print("..........")
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_d,end_y,grid_size,grid_size))
                    if starting_x_d +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_d,height-parking_lot_height,parking_lot_width,parking_lot_height,0,False))
                    #print(starting_x_d)
                    line=int(end_y/grid_size)
                    col=int(starting_x_d/grid_size)
                    #print(line)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_d+= parking_lot_width + parking_line_Width
                    
                    #print("..........")

                starting_y_u+=grid_size
                end_y+=grid_size
                counter+=1
            #i,j=0,0
            #while j < (height/grid_size):
             #   while i < (width/grid_size):
              #      pygame.draw.rect(self.board,(255,255,255),(i*grid_size,j*grid_size,grid_size,grid_size))
               #     i+=parking_lot_width/grid_size
        # horizontal park        
        elif(self.parking_technique==1):
            end_y=height-parking_lot_width
            while starting_y_u < parking_lot_width:
                starting_x_u=0
                starting_x_d=0
                while starting_x_u < width : 
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_u,starting_y_u,grid_size,grid_size))
                    if starting_x_u +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_u,0,parking_lot_height,parking_lot_width,0,False))
                    line=int(starting_y_u/grid_size)
                    col=int(starting_x_u/grid_size)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_u+= parking_lot_height + parking_line_Width
                    
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_d,end_y,grid_size,grid_size))
                    if starting_x_d +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_d,height-parking_lot_width,parking_lot_height,parking_lot_width,0,False))
                    line=int(end_y/grid_size)
                    col=int(starting_x_d/grid_size)
                    #print(line)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_d+= parking_lot_height + parking_line_Width
                    
                    pygame.display.update()
                    
                starting_y_u+=grid_size
                end_y+=grid_size
                counter+=1
                
        self.goal_state=self.generateGoal()
        self.obstacles=self.generateObstacles(10)

        self.drawGoal(self.goal_state)
        self.draw_obstacles()
        pygame.display.update()
    
    def env1(self):
        starting_x_u=-1
        starting_y_u=0
        line=0 
        col=0 
        starting_x_d=-1
        counter=0

        #vertical park
        if(self.parking_technique==0):
            
            end_y=height-parking_lot_height
            
            while starting_y_u < parking_lot_height:
                starting_x_u=0
                starting_x_d=0
                while starting_x_u<(width) and starting_x_d<(width):
                    pygame.display.update()
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_u,starting_y_u,grid_size,grid_size))
                   # print(".........")
                    #print(starting_x_u)
                    if starting_x_u +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_u,0,parking_lot_width,parking_lot_height,0,False))
                    line=int(starting_y_u/grid_size)
                    col=int(starting_x_u/grid_size)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_u+= parking_lot_width + parking_line_Width
                    #print("..........")
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_d,end_y,grid_size,grid_size))
                    if starting_x_d +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_d,height-parking_lot_height,parking_lot_width,parking_lot_height,0,False))
                    #print(starting_x_d)
                    line=int(end_y/grid_size)
                    col=int(starting_x_d/grid_size)
                    #print(line)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_d+= parking_lot_width + parking_line_Width
                    
                    #print("..........")

                starting_y_u+=grid_size
                end_y+=grid_size
                counter+=1
            #i,j=0,0
            #while j < (height/grid_size):
             #   while i < (width/grid_size):
              #      pygame.draw.rect(self.board,(255,255,255),(i*grid_size,j*grid_size,grid_size,grid_size))
               #     i+=parking_lot_width/grid_size
        # horizontal park        
        elif(self.parking_technique==1):
            end_y=height-parking_lot_width
            while starting_x_u < parking_lot_width:
                starting_x_u=0
                starting_x_d=0
                while starting_x_u < width : 
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_u,starting_y_u,grid_size,grid_size))
                    if starting_x_u +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_u,0,parking_lot_height,parking_lot_width,0,False))
                    line=int(starting_y_u/grid_size)
                    col=int(starting_x_u/grid_size)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_u+= parking_lot_height + parking_line_Width
                    
                    pygame.draw.rect(self.board,(255,255,255),(starting_x_d,end_y,grid_size,grid_size))
                    if starting_x_d +grid_size < width and counter < 1:
                        self.lots.append(ParkingLot(starting_x_d,height-parking_lot_width,parking_lot_height,parking_lot_width,0,False))
                    line=int(end_y/grid_size)
                    col=int(starting_x_d/grid_size)
                    #print(line)
                    gridcells.ADJList[line*int(width/grid_size)+col].color='White'
                    starting_x_d+= parking_lot_height + parking_line_Width
                    
                    pygame.display.update()
                    
                starting_y_u+=grid_size
                end_y+=grid_size
                counter+=1
                
        self.goal_state=self.generateGoal()
        self.generate_full_lots(2)
        self.draw_lots()
        self.obstacles=self.generateObstacles(10)


        self.drawGoal(self.goal_state)
        self.draw_obstacles()
        pygame.display.update()
            
        ##-------------------------------------end of env instances ----------------------------     
    
    def move_car_along_path(self,path_points, speed):
        path_points = list(reversed(path_points))  # Reverse the path_points and convert to a list
        n = len(path_points)
    
        for i in range(n- 1):
            start_point = path_points[i]
            end_point = path_points[i + 1]
            distance = math.sqrt((end_point.x - start_point.x) ** 2 + (end_point.y - start_point.y) ** 2)
            if distance==0 :
                continue  
            
            steps = int(distance / speed)  # Calculate the number of steps based on speed
            for step in range(steps + 1):
                intermediate_x = start_point.x + (end_point.x - start_point.x) * step / (steps)
                intermediate_y = start_point.y + (end_point.y - start_point.y) * step / (steps)
                self.draw_car_at_point((intermediate_x, intermediate_y))  # Draw the car at its updated position
                self.car.centerx=(intermediate_x)
                self.car.centery=(intermediate_y)
                pygame.display.update() 
                pygame.time.delay(speed)  # Delay to control the speed of movement
            
                self.draw_gridcells()
                self.draw_obstacles()
            self.drawGoal(self.goal_state)
            if end_point.x==self.goal_state[0] and end_point.y==self.goal_state[1]:
              break
        self.draw_path(path_points,(100,0,0),3)


    def generate_full_lots(self,num):
        count=0
        while count<num:
            lot = self.lots[random.randint(0, len(self.lots) - 1)]
            if( not lot.isgoal and not lot.full):
                lot.full=True
                count+=1

        
    def draw_lots(self):
        for lot in self.lots:
            rand=random.randint(0, 1)
            if lot.full and not lot.isgoal:
                color = (255, 0, 0)  # Red color for occupied parking lots
                err=random.randint(-40,40)
                for j in range(int(lot.y),int(lot.y+lot.height), grid_size):
                    for i in range(int(lot.x),int(lot.x + lot.width) -1, grid_size):
                            gridcells.ADJList[int((i/grid_size) + (width/grid_size)*(j/grid_size))].color='Red'
                            if rand==1:
                                pygame.draw.rect(self.board,color,(i+err,j,grid_size,grid_size))
                            else:
                                pygame.draw.rect(self.board,color,(i,j+err,grid_size,grid_size))
                            pygame.display.update()
    def draw_car_at_point(self, pos):
        # Clear the previous position of the car
        pygame.draw.rect(self.board, (0, 0, 0), (self.car.centerx-grid_size , self.car.centery - grid_size, car_length, car_width))  
        #self.draw_path(path_points,(100,0,0),3)
        pygame.draw.rect(self.board, (250, 0, 110), (pos[0]-grid_size, pos[1]-grid_size, car_length, car_width))
        
        # Update the display for the entire board surface
        pygame.display.update()
    

    # Clear the previous position of the car
    #pygame.time.delay(2)
    # Draw the car at its new position
    #pygame.draw.rect(self.board, (250, 0, 110), (self.car.centerx-grid_size , self.car.centery -grid_size, car_length, car_width))  
        
    
    def get_cell_at_position(self, x, y):
        for cell in gridcells.ADJList:
            if cell.x == x and cell.y == y:
                return cell
        return None
    
    def is_clear_pathRRT(self, start_node, end_node):
        x1, y1 = start_node.x, start_node.y
        x2, y2 = end_node.x, end_node.y
        #print("start",start_node.nodeCode)
        #print("end",end_node.nodeCode)

        min_x = int(min(x1, x2))
        max_x = int(max(x1, x2))
        min_y = int(min(y1, y2))
        max_y = int(max(y1, y2))

        car_width_cells = math.ceil(car_width / grid_size)  # Number of cells occupied by car width
        car_height_cells = math.ceil(car_length / grid_size)  # Number of cells occupied by car height
       
           
        for x in range( min_x - (car_width_cells - 1) * grid_size, max_x + (car_width_cells-1) * grid_size +1, grid_size):
            for y in range(min_y - (car_height_cells - 1) * grid_size, max_y +(car_height_cells-1) * grid_size +1, grid_size):
                cell = self.get_cell_at_position(x, y)
                if cell!=None:
                    #print(cell.nodeCode)
                if cell is not None and (cell.color == 'Blue' or cell.color == 'White' or cell.color == 'Red'):
                    #print('obstacle' ,cell.nodeCode)
                    return False
        #print('--------')
        return True
    
    def is_clear_pathA_star(self,start_node, end_node):
        
        x1, y1 = start_node.x, start_node.y
        x2, y2 = end_node.x, end_node.y

        min_x = int(min(x1, x2))
        max_x = int(max(x1, x2))
        min_y = int(min(y1, y2))
        max_y = int(max(y1, y2))

        car_width_cells = math.ceil(car_width / grid_size)  # Number of cells occupied by car width
        car_height_cells = math.ceil(car_length / grid_size)  # Number of cells occupied by car height

        for x in range(min_x - int((car_width_cells - 1) * grid_size), max_x + int((car_width_cells-1) * grid_size) +1, grid_size):
            for y in range(min_y - int((car_height_cells - 1) * grid_size), max_y +int((car_height_cells-1) * grid_size) +1, grid_size):
                cell = self.get_cell_at_position(x, y)
                if cell!=None:
                    #print(cell.nodeCode)
                if cell is not None and (cell.color == 'Blue' or cell.color == 'White' or cell.color == 'Red'):
                    #print('obstacle' ,cell.nodeCode)
                    return False
        #print('--------')
        return True
        '''
        x1, y1 = start_node.x, start_node.y
        x2, y2 = end_node.x, end_node.y

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        # Determine the direction of movement along each axis
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        # Initialize the error term and current position
        err = dx - dy
        x, y = x1, y1
        # Calculate the size of the car in terms of grid cells
        car_width_cells = car_length / grid_size
        
    
        # Iterate over all cells along the line using Bresenham's algorithm
        while True:
            if 0 <= x < width and 0 <= y < height:
                cell = self.get_cell_at_position(x, y)
                # Check if the current cell is an obstacle or parking line
                if cell!=None and (cell.color == 'Blue' or cell.color == 'White'):
                    return False
            
             # Check for diagonal neighbors
            if 0 <= x + sx * grid_size < width and 0 <= y + sy * grid_size < height:
                cell = self.get_cell_at_position(x + sx * grid_size, y + sy * grid_size)
                if cell != None and (cell.color == 'Blue' or cell.color == 'White'):
                    return False   
            # Check if the end point has been reached
            if x == x2 and y == y2:
                break
            
            # Calculate the next position
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx * grid_size  # Adjust the step size based on the grid size
            if e2 < dx:
                err += dx
                y += sy * grid_size  # Adjust the step size based on the grid size

        return True 
        '''
    
    def find_path(self,start_nod,goal_node, path_color, line_width):
        curr_node = goal_node

        while curr_node != None and curr_node.nodeCode is not start_nod.nodeCode:
            #print(curr_node.nodeCode)
            path_points.append(curr_node)
            curr_node = curr_node.parent
        
        if(curr_node!=None):
            path_points.append(curr_node)
        
        return path_points  
    
    def draw_path(self, path_points ,path_color, line_width):
           # Draw the path
        for i in range(len(path_points) - 1):
            pygame.draw.line(self.board, path_color, (path_points[i].x,path_points[i].y), (path_points[i + 1].x,path_points[i + 1].y), line_width)    
            pygame.display.update()   
            
    def  drawEdges(self,edges):
        for i, edge in enumerate(edges):
            # Decrease red component gradually, ensuring it stays within the valid range
            red_component = max(0, 255 - i % 256)
            color = (red_component, 192, 203)
            pygame.draw.line(self.board, color, (edge[0].x, edge[0].y), (edge[1].x, edge[1].y), 2)
    
    def generateGoal(self):
        i=random.randint(0, len(self.lots) - 1)
        goal = self.lots[i]
        goal.isgoal=True
        park_topleft_x=goal.x
        park_topleft_y=goal.y
        park_width=goal.width
        park_height=goal.height
        return (park_topleft_x + park_width/2 , park_topleft_y + park_height/2 , park_width , park_height)
        
        
    def drawGoal(self,goal): 
        park_topleft_y=goal[1]   
        park_topleft_x=goal[0]
        park_width=goal[2]
        park_height=goal[3]
        for j in range(int(park_topleft_y-park_height/2),int(park_topleft_y+park_height/2), grid_size):
            for i in range(int(park_topleft_x-park_width/2),int(park_topleft_x + park_width/2) -1, grid_size):
                gridcells.ADJList[int((i/grid_size) + (width/grid_size)*(j/grid_size))].color="Green"
                pygame.draw.rect(self.board,(50,100,100),(i,j,grid_size,grid_size))
        
    
    def generateObstacles(self,number):
        count=0
        obstacles=[]
        while count < number:
            randomcell=gridcells.ADJList[random.randint(0,499)]
            if randomcell.color=='Black':
                # Check if the random cell is within the goal lot area
                # goal_state = [goal.x , goaL.y , goal.width, goal.height]
                if self.goal_state[0] - self.goal_state[2] / 2 < randomcell.x < self.goal_state[0] + self.goal_state[2] / 2 :
                  if self.goal_state[1] - self.goal_state[3] / 2 < randomcell.y < self.goal_state[1] + self.goal_state[3] / 2:
                    continue  # Skip this iteration if the cell is within the goal lot area
                randomcell.color='Blue'
                obstacles.append(Obstacles(randomcell.x-grid_size/2,randomcell.y-grid_size/2,grid_size,grid_size))
                count+=1
        return obstacles
    
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.board, (100, 100, 200), (obstacle.x, obstacle.y, obstacle.width, obstacle.height))
