# This is the code for the uniform cost search (A* with h(n) hardocded to equal zero)
import copy
from copy import deepcopy

queue = []

A = [[1, 2, 3], 
    [4, 5, 6],
    [7, 8, 0]]

B = [[1, 2, 3], 
    [4, 5, 6],
    [0, 7, 8]]

C = [[1, 2, 3], 
    [4, 0, 6],
    [7, 5, 8]]

D = [[0, 1, 3], 
    [4, 2, 6],
    [7, 5, 8]]

E = [[1, 2, 3], 
    [4, 5, 6],
    [7, 0, 8]]

# queue.append(A)
# queue.append(B)

# for i in range(len(queue)): #for every board in the queue
#     for j in range(3): #for every row in board
#             print(str(queue[i][j][0]) + ' ' + str(queue[i][j][1]) + ' ' + str(queue[i][j][2])) 
#     print('----------')
    
# print(queue)

# print (str(queue[i]))
# print("A[0][0]: " + str(A[0][0]))


# function general-search(problem, QUEUEING-FUNCTION)
#     nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
  
#     loop do
#         if EMPTY(nodes) then return "Failure" # We have proved there is no solution  
#         node = REMOVE-FRONT(nodes) 
#         if problem.GOAL-TEST(node.STATE) succeeds then return node 
#         nodes = QUEUEING-FUNCTION(nodes,EXPAND(node,problem.OPERATORS))  
#     end loop

########################################################

# class problem:
#     initialState = []

# def queueingFunction():
#     print("TODO")
    ## combine the passed in queue, and add to it the expansion of the current node

# def expand(node): #need to add problem.operators, but confused as to what operators there are
#     print("TODO")

# def makeNode(node):
#     print("TODO")
    # return single matrix/list

# def makeQueue():
#     print("TODO")
    # return queue that contains a single list as the initial state



class Problem: # used in 'main' when creating an initial problem
    def __init__(self, initialState):
        self.initialState = initialState
        self.operators = [[-1,0], [1, 0], [0,-1], [0,1]]
        self.goalState = [[1, 2, 3], 
                         [4, 5, 6],
                         [7, 8, 0]]

    def printBoard(self):
        for j in range(3): # for every row in board
            print(str(self.initialState[j][0]) + ' ' + str(self.initialState[j][1]) + ' ' + str(self.initialState[j][2]))

    def goalTest(self, currState):
        if currState == self.goalState:
            return True

class Node:
    def __init__(self, initialState):
        self.state = initialState
        self.dimension = len(initialState[0])
        self.depth = 0                                  # can increment every time another one is created
        self.heuristic = 0                              # used in the heuristic
    def printBoard(self):
        for j in range(3):                              # for every row in board
            print(str(self.state[j][0]) + ' ' + str(self.state[j][1]) + ' ' + str(self.state[j][2]))

class NodeQueue:
    def __init__(self, initialNode):
        self.queue = []
        self.queue.append(initialNode)
        
    def printBoard(self):
        for i in self.queue:
            for j in range(3):                          # for every row in board
                print(str(i.state[j][0]) + ' ' + str(i.state[j][1]) + ' ' + str(i.state[j][2]))
        
    def concat(self, newNodes):
        concatination = newNodes + self.queue
        self.queue = concatination

def findBlank(state):
    listNum = 0
    indexNum = 0
    for list in state:
        for index in list:
            if index == 0:
                return [listNum, indexNum]
            indexNum = indexNum + 1
        listNum = listNum + 1
        indexNum = 0

def expand(node, operators):
    max = node.dimension - 1
    children = []
    swaps = []                                                      # New positions that blank can go to
    blankLocation = findBlank(node.state)

    for move in operators:
        x = blankLocation[0] - move[0]
        y = blankLocation[1] - move[1]
        if (x >= 0 and x <= max) and (y >= 0 and y <= max):
            swaps.append([x,y])
    for i in swaps:                                                 # For every new location the blank can go to
        child = copy.deepcopy(node)                                 # Creates a deepcopy of the passed in node
        child.depth = child.depth + 1                               # Adds to depth as it is a new child on the tree

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
    if flag == 1:
        for i in newNodes:
            if i.state in duplicates:
                newNodes.remove(i)
            else:
                duplicates.append(i.state)
        prevNodes.concat(newNodes)
        return prevNodes
    elif flag == 2:
        print("TODO: misplaced tile function")
    elif flag == 3:
        print("TODO: manhattan distance function")

def generalSearch(Problem, queueingFunctionFlag):
    rootNode = Node(Problem.initialState)
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
        x = x + 1
        # print("queueingFunction called")
    return False


Problem = Problem(D)
duplicates = [Problem.initialState]

Result = generalSearch(Problem, 1)
if Result == False:
    print("Failed to find a solution")
else:
    Result.printBoard()
    print("Result.depth: " + str(Result.depth))