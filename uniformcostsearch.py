# This is the code for the uniform cost search (A* with h(n) hardocded to equal zero)
import copy
from copy import deepcopy

queue = []

A = [[1, 2, 3], # 0
    [4, 5, 6],
    [7, 8, 0]]

B = [[1, 2, 3], 
    [4, 5, 6],  # 2
    [0, 7, 8]]

C = [[1, 2, 3], 
    [5, 0, 6],  # 4
    [4, 7, 8]]

D = [[1, 3, 6], 
    [5, 0, 2],  # 8
    [4, 7, 8]]

E = [[1, 3, 6], 
    [5, 0, 7],  # 12
    [4, 8, 2]]

F = [[1, 6, 7], # 16
    [5, 0, 3],
    [4, 8, 2]]

G = [[7, 1, 2], 
    [4, 8, 5],  # 20
    [6, 3, 0]]

H = [[0, 7, 2], # 24
    [4, 6, 1],
    [3, 5, 8]]

I = [[8, 6, 7], # 31
    [2, 5, 4],
    [3, 0, 1]]

class Problem: # used in 'main' when creating an initial problem
    def __init__(self, initialState):
        self.initialState = initialState
        self.dimension = len(initialState[0])
        self.operators = [[-1,0], [1, 0], [0,-1], [0,1]]
        self.goalState = [[1, 2, 3], 
                         [4, 5, 6],
                         [7, 8, 0]]

    def printBoard(self):
        for i in range(self.dimension):                              # for every row in board
            for j in range(self.dimension):
                print(str(self.initialState[i][j]) + ' ', end='')
            print('')

    def goalTest(self, currState):
        if currState == self.goalState:
            return True

class Node:
    def __init__(self, initialState):
        self.goalState = [[1, 2, 3], 
                         [4, 5, 6],
                         [7, 8, 0]]
        self.state = initialState
        self.dimension = len(initialState[0])
        self.g = 0                                  # can increment every time another one is created
        self.h = 0                                  # used in the heuristic
        self.f = 0
        
    def printBoard(self):
        print('g: ' + str(self.g))
        print('h: ' + str(self.h))
        print('f: ' + str(self.f))
        for i in range(self.dimension):                              # for every row in board
            for j in range(self.dimension):
                print(str(self.state[i][j]) + ' ', end='')
            print('')

    def calcF(self):
        self.f = self.h + self.g

    def misplacedTile(self):
        # Calculates the misplaced tile heuristic
        # print("Misplaced Tile")
        hVal = 0
        for i in range(self.dimension):                              # for every row in board
            for j in range(self.dimension):
                if self.state[i][j] != self.goalState[i][j]:
                    hVal = hVal + 1
        self.h = hVal - 1

    def manhattanDistance(self):
        # Calculates the Manhattan Distance heuristic

        hVal = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if (self.state[i][j] != self.goalState[i][j]) and (self.state[i][j] != 0): 
                    goalLocation = findNum(self.goalState, self.state[i][j])    # goalLocation is the location on the goalstate of the number we have

                    #Subtrack self.state[i][j] - goalLocation
                    difference = [i - goalLocation[0], j - goalLocation[1]]

                    #abs value of difference list
                    difference[0] = abs(difference[0])
                    difference[1] = abs(difference[1])

                    #add both list items together
                    hVal = hVal + (difference[0] + difference[1])                    
        self.h = hVal

class NodeQueue:
    def __init__(self, initialNode):
        self.queue = []
        self.queue.append(initialNode) 
        
    def printBoard(self):
        for i in self.queue:
            print('g: ' + str(i.g))
            print('h: ' + str(i.h))
            print('f: ' + str(i.f))        
            for j in range(3):                          # for every row in board
                print(str(i.state[j][0]) + ' ' + str(i.state[j][1]) + ' ' + str(i.state[j][2]))
        
    def concat(self, newNodes):
        concatination = newNodes + self.queue
        self.queue = concatination

def maxQueue(length):
    global maxQueueLength
    if length > maxQueueLength:
        maxQueueLength = length

def findNum(state, num):                                # Returns the location in a list of the number and state passed in
    listNum = 0
    indexNum = 0
    for list in state:
        for index in list:
            if index == num:
                return [listNum, indexNum]
            indexNum = indexNum + 1
        listNum = listNum + 1
        indexNum = 0

def expand(node, operators):
    max = node.dimension - 1
    children = []
    swaps = []                                                      # New positions that blank can go to
    blankLocation = findNum(node.state, 0)

    for move in operators:
        x = blankLocation[0] - move[0]
        y = blankLocation[1] - move[1]
        if (x >= 0 and x <= max) and (y >= 0 and y <= max):
            swaps.append([x,y])
    for i in swaps:                                                 # For every new location the blank can go to
        child = copy.deepcopy(node)                                 # Creates a deepcopy of the passed in node
        child.g = child.g + 1                               # Adds to depth as it is a new child on the tree

        tempVal = child.state[i[0]][i[1]]                           # Saves the value on the board that the blank is switching with
        child.state[i[0]][i[1]] = 0                                 # Sets the switched possition to blank value (0) and sets 
        child.state[blankLocation[0]][blankLocation[1]] = tempVal   # Sets the original blank spot to temp value, indicating a switch has taken place

        children.append(child)                                      # Appends new child to child list
    return children

def queueingFunction(flag, prevNodes, newNodes):
    global duplicates
    # print("duplicates:")
    # for k in duplicates:
    #     print(str(k))
    for i in newNodes:
        if i.state in duplicates:
            newNodes.remove(i)
        else:
            duplicates.append(i.state)
    
    # print("prevNodes:")
    # prevNodes.printBoard()
    if flag == 1:
        prevNodes.concat(newNodes)
        return prevNodes
    elif flag == 2:
        # print("TODO: misplaced tile function")
        for j in newNodes:
            j.misplacedTile()
            j.calcF()

        prevNodes.concat(newNodes)
        prevNodes.queue.sort(key=lambda j: j.f, reverse=True)
        # print("prevNodes:")
        # prevNodes.printBoard()
        return prevNodes
    elif flag == 3:
        # print("TODO: manhattan distance function")
        for j in newNodes:
            # print("j: " + str(j.state))
            j.manhattanDistance()
            j.calcF()       
        
        prevNodes.concat(newNodes)
        prevNodes.queue.sort(key=lambda j: j.f, reverse=True)
        # print("prevNodes:")
        # prevNodes.printBoard()
        # print("winner's f:" + str((prevNodes.queue[-1]).f))
        winnerF = (prevNodes.queue[-1]).f
        tieBreakers = []
        for k in reversed(prevNodes.queue):
            if k.f == winnerF:
                tieBreakers.append(prevNodes.queue.pop())
            else:
                break
        tieBreakers.sort(key=lambda j: j.g, reverse=True)
        prevNodes.queue = prevNodes.queue + tieBreakers
        return prevNodes

def generalSearch(Problem, queueingFunctionFlag):   # Could pass the queinngFunctionFlag as an attribute of problem, 
    rootNode = Node(Problem.initialState)           # and when you make the root node make it an attribute of Node
    print("rootNode: " + str(rootNode.state))

    nodes = NodeQueue(rootNode)

    x = 0
    while nodes:                                                                # While the queue of nodes is not empty
        currNode = nodes.queue.pop()                                            # Gets the top node off of the queue
        print("currNode:")
        currNode.printBoard()
        if Problem.goalTest(currNode.state):
            print("Found the goal state!")
            print("interation: " + str(x))
            return currNode
        nodes = queueingFunction(queueingFunctionFlag, nodes, expand(currNode, Problem.operators))    # need to add problem.operators but still confused

        maxQueue(len(nodes.queue))
        x = x + 1
    return False

Problem = Problem(G)
duplicates = [Problem.initialState]
maxQueueLength = 0

Result = generalSearch(Problem, 1)
if Result == False:
    print("Failed to find a solution")
else:
    Result.printBoard()
    print("Result.depth: " + str(Result.g))
    print("Max Queue Length: " + str(maxQueueLength))
    
# A = [[1, 2, 3], # 0
#     [4, 5, 6],
#     [7, 8, 0]]

# B = [[1, 2, 3], 
#     [4, 5, 6],  # 2
#     [0, 7, 8]]

# C = [[1, 2, 3], 
#     [5, 0, 6],  # 4
#     [4, 7, 8]]

# D = [[1, 3, 6], 
#     [5, 0, 2],  # 8
#     [4, 7, 8]]

# E = [[1, 3, 6], 
#     [5, 0, 7],  # 12
#     [4, 8, 2]]

# F = [[1, 6, 7], # 16
#     [5, 0, 3],
#     [4, 8, 2]]

# G = [[7, 1, 2], 
#     [4, 8, 5],  # 20
#     [6, 3, 0]]

# H = [[0, 7, 2], # 24
#     [4, 6, 1],
#     [3, 5, 8]]

# I = [[8, 6, 7], # 31
#     [2, 5, 4],
#     [3, 0, 1]]