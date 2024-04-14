from AdjList import *
from Environment import *
from sensory import *
from Astar import *
from RRT import *
import pygame

        
class Main:                  
    def main():
  ####################################################################    
      #this is main part for A* algorithm
  ####################################################################
        '''
        ######### for first environment #############
        sum=0
        start=time.time()
        env=Environment(4,0)
        env.env0()
        astar=Astar(env)
        t_goal=astar.Astar_Alg() # time that Astar algorithm returns, 
                                    # actual time it takes to find goal state
                                    # (without including time spent for movement of car)
        end=time.time()
        sum=(end-start)
        print('time spent to find goal state: ', t_goal)
        print('time spent in total: ', sum)
        '''
        
        
        ######### for second environment #############
        sum=0
        start=time.time()
        env=Environment(4,0)
        env.env1()
        astar=Astar(env)
        t_goal=astar.Astar_Alg() # time that Astar algorithm returns, 
                                    # actual time it takes to find goal state
                                    # (without including time spent for movement of car)
        end=time.time()
        sum+=(end-start)
        time.sleep(0.01)
        print('time spent to find goal state: ', t_goal)
        print('time spent in total: ', sum)
        
        
  ######################################################################  
    
    # this is the main part for RRT algorithm
  #####################################################################
        '''
        ###### for first environment #############
        sum=0
        start=time.time()
        env=Environment(4,0)
        env.env0()
        rrt=RRT(env)
        t_goal=rrt.RRT_Alg() # time that Astar algorithm returns, 
                                    # actual time it takes to find goal state
                                    # (without including time spent for movement of car)
        end=time.time()
        sum=(end-start)
        print('time spent to find goal state: ', t_goal)
        print('time spent in total: ', sum)   
        
        '''
        '''
        ######### for second environment #############
        sum=0
        start=time.time()
        env=Environment(4,0)
        env.env1()
        rrt=RRT(env)
        t_goal=rrt.RRT_Alg() # time that Astar algorithm returns, 
                                    # actual time it takes to find goal state
                                    # (without including time spent for movement of car)
        end=time.time()
        sum=(end-start)
        print('time spent to find goal state: ', t_goal)
        print('time spent in total: ', sum)
        '''
        
        ## please do not commnet while loop here, otherwise you will not be able to load the window
        running=True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
       

            
        
    if __name__ == "__main__":
        #for i in range(0,10):
         main()
