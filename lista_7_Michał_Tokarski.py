from graphviz import Digraph
import sys
class Vertex:
    def __init__(self,key):
        self.id = key
        self.color = 'white'
        self.pred = None
        self.dist = sys.maxsize
        self.connectedTo = {}   #lista sąsiedztwa z wagami

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
    
    def setDistance(self,d):
        self.dist = d
        
    def getColor(self):
        return self.color

    def setColor(self,color):
        self.color = color    

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()
    
    def getDistance(self):
        return self.dist
    
    def setPred(self,p):
        self.pred = p

    def getPred(self):
        return self.pred

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

        

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()
#zadanie 2    
    def view(self, filename: str = "graph.txt") -> str:
        dot = Digraph()
        for vertex in self.getVertices():
            dot.node(str(vertex),str(vertex))
        for vertex in self.getVertices():
            for neighbor in self.getVertex(vertex).getConnections():
                neighbor = neighbor.getId()
                dot.edge(str(vertex),str(neighbor))
        
        with open(filename, 'w') as graph_file:
            graph_file.write(dot.source)
        return dot.source
#zadanie 3
    def bfs(self, start):
        for vertex in self.vertList.values():
            vertex.setColor('white')
        start.setDistance(0)
        start.setPred(None)
        queue = []
        queue.append(start)
        while len(queue):
            vertex = queue.pop(0)
            for neighbor in vertex.getConnections():
                if neighbor.getColor() == 'white':
                    neighbor.setColor('gray')
                    neighbor.setDistance(vertex.getDistance() + 1)
                    neighbor.setPred(vertex)
                    queue.append(neighbor)
            vertex.setColor('black')

                
#zadanie 3 i 4
    def dfs(self, sort):
        if sort:
            topological = []
        for vertex in self.vertList.values():
            vertex.setColor('white')
        for start in self.vertList.values():
            stack = [start]
            if sort:
                temp = []
            while len(stack) > 0:
                vertex = stack[-1]
                if vertex.getColor() == 'white':
                    vertex.setColor('gray')
                    for neighbor in vertex.getConnections():
                        if neighbor.getColor() == 'white':
                            stack.append(neighbor)
                        elif sort and neighbor.getColor() == 'gray':
                            raise Exception('there is a cycle in the graph')
                if vertex.getColor() == 'gray' and vertex.getId() == stack[-1].getId():
                    vertex.setColor('black')
                    if sort:
                        temp.insert(0, stack.pop().getId())
                elif vertex.getColor() == 'black':
                    stack.pop()
            if sort:
                topological = temp + topological
        if sort:
            return topological
#zadanie 5
    def findShortest(self, start, stop):
        """Method that finds shortest path from one node to another/"""

        steps = f"{start}"
        stepsList = []
        startVert = self.getVertex(start)
        self.bfs(startVert)
        endVert = self.getVertex(stop)
        while endVert.getPred():
            stepsList.append(endVert.getId())
            endVert = endVert.getPred()
        
        stepsList.append(endVert.getId())
        stepsList = stepsList[-2:-1-len(stepsList):-1]
        for step in stepsList:
            steps += f" -> {step}"
        
        steps.rstrip
        return steps
        



    def __iter__(self):
        return iter(self.vertList.values())
#Z tego co pamiętam należało zrobić jedno zadanie spośród 6/7. Zrobiłem 6.
def legal(x, y, max_x, max_y):
    """Args:    x -- Missionaries at one coast
                y -- Cannibals at one coast
                max_x -- Total amount of missionaries
                max_y -- Total amount of cannibals"""
    if x >= 0 and y >= 0 and x <= max_x and y <= max_y:
        if (max_x-x == 0 or max_x - x >= max_y - y) and (x == 0 or x >= y):
            return True  
        else:
            return False   
    else:
        return False
 

def legal_moves(x, y, boat, max_x, max_y):
    """Returns all legal moves
    Args:   x -- Missionaries at one coast
            y -- Cannibals at one coast
            max_x -- Total amount of missionaries
            max_y -- Total amount of cannibals
            boat - Position of boat"""
    new_state = []
    moves = [(1, 0, 1), (2, 0, 1), (0, 1, 1), (0, 2, 1), (1, 1, 1)]
    for i in moves:
        if boat == 0:
            x1 = x + i[0]
            y1 = y + i[1]
            boat1 = 1
            
        else:
            x1 = x - i[0]
            y1 = y - i[1]
            boat1 = 0
            
        if legal(x1, y1, max_x, max_y):
            new_state.append((x1, y1, boat1))


    return new_state

def missionaries_and_canibals(missionaries = 3, cannibals = 3):
    g = Graph()
    moves = [(missionaries, cannibals, 1)]
    start = 0
    stop = len(moves)
    while True:
        for i in range(start, stop):
            state = moves[i]
            for j in legal_moves(*state[0:3], missionaries, cannibals):
                g.addEdge(state, j)
                if j not in moves:
                    moves.append(j)
                
            
        
        if stop == len(moves):
            break

        start = stop - 1
        stop = len(moves)
    
    return g




graph = Graph()
graph.addEdge(1, 2)
graph.addEdge(1, 3)
graph.addEdge(2, 4)
graph.addEdge(3, 4)
graph.addEdge(2, 5)
graph.addEdge(3, 6)
graph.addEdge(1, 4)
graph.addEdge(6, 7)
graph.addEdge(5, 8)
graph.addEdge(6, 8)
graph.addEdge(8, 9)
graph.addEdge(2, 9)
graph.view()
print(graph.findShortest(1, 5))
graph_new = missionaries_and_canibals(3, 3)
print(graph_new.findShortest((3, 3, 1), (0, 0, 0)))