import time
import copy
from copy import deepcopy

class Problem:
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
        hVal = 0
        for i in range(self.dimension):                              # for every row in board
            for j in range(self.dimension):
                if self.state[i][j] != self.goalState[i][j]:
                    hVal = hVal + 1
        self.h = hVal - 1

    def manhattanDistance(self):
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

# queueing function takes in the flag for the chosen algorithm, the current nodes in the queue, and the children nodes
def queueingFunction(flag, prevNodes, newNodes):
    # creates a list that stores all of the duplicate states
    global duplicates
    # iterates through the child nodes
    for i in newNodes:
        # if the current child state in the list of child states is found in the duplicates list, take it out of the child list
        if i.state in duplicates:
            newNodes.remove(i)
        else:
            duplicates.append(i.state)
    if flag == 1:
        prevNodes.concat(newNodes)
        return prevNodes
    elif flag == 2:
        for j in newNodes:
            j.misplacedTile()
            j.calcF()
        prevNodes.concat(newNodes)
        prevNodes.queue.sort(key=lambda j: j.f, reverse=True)
        return prevNodes
    elif flag == 3:
        for j in newNodes:
            j.manhattanDistance()
            j.calcF()       
        prevNodes.concat(newNodes)
        prevNodes.queue.sort(key=lambda j: j.f, reverse=True)
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

def generalSearch(Problem, queueingFunctionFlag): 
    # Create root node with the problem state
    rootNode = Node(Problem.initialState)          
    print("rootNode: " + str(rootNode.state))

    # Create a queue of Nodes, initialized with the root node
    nodes = NodeQueue(rootNode)

    # x keeps track of the iterations
    x = 0
    # loops while the nodes list is not empty
    while nodes:                                                                
        # pops the top of the queue off and uses that as the current node, this node is also the most efficientg
        currNode = nodes.queue.pop()                                            
        print("currNode:")
        currNode.printBoard()
        # checks the current node's state, enters conditional if it is the goal state
        if Problem.goalTest(currNode.state):
            print("Found the goal state!")
            print("interation: " + str(x))
            return currNode
        # calls the queueing function, passes in the flag for the type of queueing function, the original nodes,
        # and the expanded children. The expand function uses the current node and the problem operators
        nodes = queueingFunction(queueingFunctionFlag, nodes, expand(currNode, Problem.operators))    # need to add problem.operators but still confused

        # calls maxQueue function which updates maxQueue variable to keep track of the maxQueue
        maxQueue(len(nodes.queue))
        # increases the iteration
        x = x + 1
    return False


def userInput():
    # Call global so we can write to the variables
    global Problem
    global Result
    global duplicates

    print("Welcome to Luccap's 8-puzzle solver.Type “1” to use a default puzzle, or “2” to enter your own puzzle.")
    puzzleSelection = input()
    puzzleSelection = int(puzzleSelection)
    if puzzleSelection == 1:
        algoChoice = input("Enter your choice of algorithm:\n1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic\n3. A* with the Manhattan distance heuristic\n")
        # Creates the Problem object by passing in the default game board
        Problem = Problem(D)
        # Adds the first state to the list of duplicates
        duplicates = [Problem.initialState]
        # Starts program timer
        t0 = time.time()
        # Runs general search algorithm and returns the result node/boolean
        Result = generalSearch(Problem, int(algoChoice))
        # Ends program timer
        t1 = time.time()
        # Calculate time elapsed
        totalTime = t1-t0
        print("Time elapsed: " + str(totalTime))
        return Result
    elif puzzleSelection == 2:
        print("Enter your puzzle, use a zero to represent the blank")
        print("Enter the first row, use space or tabs between numbers")
        firstRow = input()
        print("Enter the second row, use space or tabs between numbers")
        secondRow = input()
        print("Enter the third row, use space or tabs between numbers")
        thirdRow = input()
        
        # Take string inputs, split them into strings, and then map the strings to ints, finally putting them all in a list
        x = [list(map(int, firstRow.split())), list(map(int, secondRow.split())), list(map(int, thirdRow.split()))]
        Problem = Problem(x)
        duplicates = [Problem.initialState]
        
        algoChoice = input("Enter your choice of algorithm:\n1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic\n3. A* with the Manhattan distance heuristic\n")
        
        t0 = time.time()
        Result = generalSearch(Problem, int(algoChoice))
        t1 = time.time()
        totalTime = t1-t0
        print("Time elapsed: " + str(totalTime))
        return Result

# Declaring global variables
Problem
Result = 0
duplicates = []
maxQueueLength = 0

# Creating test games of different difficulties
A = [[1, 2, 3], 
     [5, 0, 6], # 4 easy
     [4, 7, 8]]

B = [[1, 3, 6], 
     [5, 0, 7], # 12 medium
     [4, 8, 2]]

C = [[0, 7, 2], 
     [4, 6, 1], # 24 hard
     [3, 5, 8]]

D = [[8, 6, 7], 
     [2, 5, 4], # 31 impossible???
     [3, 0, 1]]

# Run Interface and program, returns a Result of a failure or the goal Node
Result = userInput()

if Result == False:
    print("Failed to find a solution")
else:
    Result.printBoard()
    print("Result.depth: " + str(Result.g))
    print("Max Queue Length: " + str(maxQueueLength))