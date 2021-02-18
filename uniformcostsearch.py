import time
import copy
from copy import deepcopy

# Problem object contains the user input state, or the defaul state. Also calculates the dimension of the board, and defined the possible blank space
# moves and goal state.
# printBoard() prints the user input/default state
# goalTest() compares the passed in state to the goal state and returns True if they match
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

# Node object contains the goal state, the current state, the dimension of the game board, the depth, heuristic, and f(n) value
# printboard() prints the current node, the depth, the heuristic, and the f(n)
# calcF() sums the depth and the heuristic and sets the value to f
# misplacedTile() calculates the heuristic via misplaced tile
# manhattanDistance() calculates the heuristic via manhattan distance
class Node:
    def __init__(self, initialState):
        self.goalState = [[1, 2, 3], 
                         [4, 5, 6],
                         [7, 8, 0]]
        self.state = initialState
        self.dimension = len(initialState[0])
        self.g = 0                                  
        self.h = 0                                  
        self.f = 0
        
    def printBoard(self):
        print('g: ' + str(self.g))
        print('h: ' + str(self.h))
        print('f: ' + str(self.f))
        for i in range(self.dimension):                              
            for j in range(self.dimension):
                print(str(self.state[i][j]) + ' ', end='')
            print('')

    def calcF(self):
        self.f = self.h + self.g

    def misplacedTile(self):
        hVal = 0
        # for every tile not matching the goal state, increment hVal
        for i in range(self.dimension):                              
            for j in range(self.dimension):
                if self.state[i][j] != self.goalState[i][j]:
                    hVal = hVal + 1
        # since the heuristic is not supposed to contain the blank space, decrease it by one in the end
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

# NodeQueue object, contains a queue of nodes
# printBoard() prints all of the nodes in the queue
# concat() updates the queue to be the concatination of it with the new list of nodes
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

# checks if the queue length has grown, and if it has, updates the global max variable
def maxQueue(length):
    global maxQueueLength
    if length > maxQueueLength:
        maxQueueLength = length

# returns the location of the passed in number in a list of lists
def findNum(state, num):                                
    listNum = 0
    indexNum = 0
    for list in state:
        for index in list:
            if index == num:
                return [listNum, indexNum]
            indexNum = indexNum + 1
        listNum = listNum + 1
        indexNum = 0

# expand function returns a list of all of the possible legal child expansions of the node passed in
def expand(node, operators):
    # calculates the furthest index of the list
    max = node.dimension - 1
    # children will be the list of nodes that is returned
    children = []
    # swaps will contain all of the coordinate locations of the legal moves
    swaps = []                                                      
    # blankLocation is a list of 2 integers which show the location of the blank space
    blankLocation = findNum(node.state, 0)
    # operators are all of the legal moves the blank could make (up, down, left, and right)
    for move in operators:
        x = blankLocation[0] - move[0]
        y = blankLocation[1] - move[1]
        # checks if the calculated move is on the game board
        if (x >= 0 and x <= max) and (y >= 0 and y <= max):
            # if it is a legal move, the move's coordinates are added to swaps
            swaps.append([x,y])
    # for every new location the blank can go to
    for i in swaps:                                                 
        # creates a deepcopy of the passed in node
        child = copy.deepcopy(node)                                 
        # increments depth beacuse it is a new child node
        child.g = child.g + 1                               

        # swaps the value on the game board with the blank
        tempVal = child.state[i[0]][i[1]]                           
        child.state[i[0]][i[1]] = 0                                 
        child.state[blankLocation[0]][blankLocation[1]] = tempVal   

        # child node is appended to the list of new childs
        children.append(child)                                      
    return children

# queueing function takes in the flag for the chosen algorithm, the current nodes in the queue, and the children nodes
def queueingFunction(flag, prevNodes, newNodes):
    # creates a list that stores all of the duplicate states
    global duplicates
    # iterates through the child nodes
    for i in newNodes:
        # if the current child state is found in the duplicates list, remove it
        if i.state in duplicates:
            newNodes.remove(i)
        # otherwise, it is a new and unique state, and should be added to the duplicates list
        else:
            duplicates.append(i.state)
    # enters if uniform cost search is selected
    if flag == 1:
        # takes the new nodes, and adds them to the queue
        prevNodes.concat(newNodes)
        return prevNodes
    # enters if A* with misplaced tiles is selected
    elif flag == 2:
        # loops through the child nodes, and calculates the misplaced tile for each node. The calculated value is added as an attribute to the node
        for j in newNodes:
            j.misplacedTile()
            # calcF sums the g(n) and h(n) to get the f(n) of the misplaced tile heuristic
            j.calcF()
        # the child node list is added to the nodes queue
        prevNodes.concat(newNodes)
        # the entire list is sorted by f(n). The front of the queue has the best possible f(n) value
        prevNodes.queue.sort(key=lambda j: j.f, reverse=True)
        # winnerF contains the best possible f(n) value at the time
        winnerF = (prevNodes.queue[-1]).f
        # new list is created to contain all of the ties between the best f(n) values
        tieBreakers = []
        for k in reversed(prevNodes.queue):
            if k.f == winnerF:
                tieBreakers.append(prevNodes.queue.pop())
            else:
                break
        # this new set is sorted by depth value, having now the front of the list with the lowest depth
        tieBreakers.sort(key=lambda j: j.g, reverse=True)
        # the new set is concatinated back onto the original
        prevNodes.queue = prevNodes.queue + tieBreakers
        return prevNodes
    # enters if A* with Manhattan Distance is selected
    elif flag == 3:
    # same structure of code takes place in A* misplaced tiles
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
        # print("currNode:")
        # currNode.printBoard()
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