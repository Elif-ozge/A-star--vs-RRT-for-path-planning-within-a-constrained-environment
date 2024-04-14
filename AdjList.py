from functools import total_ordering
class MyNode:
    
    def __init__(self,x,y,parent,index,color):
        self.x=x
        self.y=y
        self.parent=parent
        self.nodeCode=index
        self.adjacencies=[]
        self.cost=0
        self.color=color
        self.heuristic=-1
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic    
      
        
class MyEdge:
    
    def __init__(self,distance,fromNode,toNode):
        self.edgecost=distance
        self.parent=fromNode
        self.child=toNode
        
class ADJLIST:
    
    def __init__(self) :
        self.ADJList=[]
        self.nodeCount=0
       
    def addNode(self,u):
        if(u!=None):
            if not self.doesNodeExist(u.nodeCode) :
                self.ADJList.append(u)
                self.nodeCount+=1
            
        else: 
            print("add node error!")
            return None
        
    def removeNode(self,u):
        try:
            for i in range(0,self.nodeCount):
                if self.doesNodeExist(i) :
                    self.removeEdge(i,u)
                
            self.ADJList[u]=None
            self.nodeCount-=1   
            return True
        except:
            print("removeNode error!")
            return False
        
    def addEdge(self,u,v):
        
        ### !!!!! sonra düzenlersin , önce path bulsun yeter
        #bu fonksiyon içerisinde eğer goal state e ulaşılmışsa  x() fonksiyonu çağırılarak sadeece en az cost'a sahip pathin 
        # son nodu goal state node'unu edges arrayinde tutabilecek şekilde düzenlenmeli böylece optimallik sağlanır
        try:
            if u!=None and v!=None:
                u.adjacencies.append(v)
                v.parent=u
                return True
        except:
            ## cannot ads an edge between nonexistent nodes
            print("addEdge error!")
            return False
        
    def removeEdge(self,u,v):
        ## here asuumed that u is fromNode(parent) and v is toNode(child)
        try:
            node_u=self.ADJList[u]
            node_v= self.ADJList[v]
            for edge in node_u.adjacencies:
                if edge.child.nodeCode == node_v.nodeCode: ###!!!!!!!!!!!!!!  <<<<< buradan şüpheliyim >>>> !!!!!!!!!!!!
                    node_u.adjacencies.remove(edge)
                    node_v.cost=-1
                    node_v.parent=None 
                    
            return True
        except:
            print("removeEdge error!")
            return False
                
        
    def doesNodeExist(self,u):
        try:
            return (self.ADJMatrix[u] != None)
        except :
            #print("nonexistent node error!")
            return False

class Main:
    
    def main():
        adj=ADJLIST()
        
        
        
        adj.addNode(0,0,0)
        adj.addNode(1,0,0)
        adj.addNode(2,0,0)
        adj.addNode(3,0,0)
        adj.addNode(4,0,0)
        
        adj.addEdge1(0,1,1)
        adj.addEdge1(1,3,3)
        adj.addEdge1(3,2,6)
        adj.addEdge1(2,4,5)
        
        adj.removeEdge(1,3)
        
       # for i in adj.ADJList:
        #   print(i.nodeCode)
        #   print(i.cost)
        #   if(i.parent==None): print("no parent!")
        #   else:
        #    print(i.parent.nodeCode)
        #print(222)
        #for k in adj.ADJList[2].adjacencies:
        #    print(k.parent.nodeCode)
        #    print(k.child.nodeCode)
        
        
    if __name__ == "__main__":
        main()