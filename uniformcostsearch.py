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

D = [[1, 0, 3], 
    [4, 2, 6],
    [7, 5, 8]]


queue.append(A)
queue.append(B)

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
        self.goalState =   [[1, 2, 3],[4, 5, 6],[7, 8, 0]]

    def printBoard(self):
        for j in range(3): # for every row in board
            print(str(self.initialState[j][0]) + ' ' + str(self.initialState[j][1]) + ' ' + str(self.initialState[j][2]))

    def goalTest(self, currState):
        if currState == self.goalState:
            return True


# Problem1 = Problem(A)
# Problem1.printBoard()
# Board2 = Problem(B)
# Board2.printBoard()

class Node:
    def __init__(self, initialState):
        self.state = initialState
        self.dimension = len(initialState[0])
        # print("self.dimension: " + str(self.dimension))
        self.depth = 0      # can increment every time another one is created
        self.goalDist = 0   # used in the heuristic
    def printBoard(self):
        for j in range(3): # for every row in board
            print(str(self.state[j][0]) + ' ' + str(self.state[j][1]) + ' ' + str(self.state[j][2]))
    
    # def makeNode(self):

class NodeQueue:
    def __init__(self, initialNode):
        self.queue = []
        self.queue.append(initialNode)
        # print("self.queue: " + str(self.queue[0]))
        
    # def makeQueue(self):
    #     return self.queue

def findBlank(state):
    listNum = 0
    indexNum = 0
    for list in state:
        for index in list:
            if index == 0:
                # print("indexNum: " + str(indexNum))
                # print("listNum: " + str(listNum))
                return [listNum, indexNum]
            indexNum = indexNum + 1
        listNum = listNum + 1
        indexNum = 0

def expand(node, operators):
    # Still don't know what the operators are...
    # I think the ops are the type of heuristic used
    # returns a list of states, at most 4, at least 2

    # movements = [[-1,0], [1, 0], [0,-1], [0,1]]
    max = node.dimension - 1
    children = []
    swaps = []                                              # New positions that blank can go to
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
    # This function takes in all of the nodes in the current queue, and then fixes them to the correct order.
    # for instance, 
    print("pushes the new nodes onto the queue")
    return []
    

def generalSearch(Problem, queueingFunctionFlag):
    rootNode = Node(Problem.initialState)
    print("rootNode: " + str(rootNode.state))

    nodes = NodeQueue(rootNode)
    print("Queue: " + str(nodes.queue[0].state))

    # childrenQueue = expand(rootNode)

    print(len(nodes.queue))
    while nodes:                                                                # While the queue of nodes is not empty
        currNode = nodes.queue.pop()                                            # Gets the top node off of the queue
        if Problem.goalTest(currNode):
            return currNode
        nodes = queueingFunction(queueingFunctionFlag, nodes, expand(currNode, Problem.operators))    # need to add problem.operators but still confused
    return False



Problem = Problem(D)
# endNode = generalSearch(Problem, "uniform")
Result = generalSearch(Problem, "uniform")
if Result == False:
    print("Failed to find a solution")
else:
    Result.printBoard()