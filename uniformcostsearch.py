# This is the code for the uniform cost search (A* with h(n) hardocded to equal zero)

queue = []

A = [[1, 2, 3], 
    [4, 5, 6],
    [7, 8, 0]]

B = [[1, 2, 3], 
    [4, 5, 6],
    [0, 7, 8]]

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
        self.operators = [-1,0,1]
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
    
    # def makeNode(self):

class NodeQueue:
    def __init__(self, initialNode):
        self.queue = []
        self.queue.append(initialNode)
        # print("self.queue: " + str(self.queue[0]))
        
    # def makeQueue(self):
    #     return self.queue

def queueingFunction(prevNodes, newNodes):
    print("pushes the new nodes onto the queue")

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

def expand(node):
    # Still don't know what the operators are...
    # I think the ops are the type of heuristic used
    # returns a list of states, at most 4, at least 2
    blankLocation = findBlank(node.state)
    print("blankLocation: " + str(blankLocation))
    print("node dimension: " + str(node.dimension))

# A = [[1, 2, 3], 
#     [4, 5, 6],
#     [7, 8, 0]]


def generalSearch(Problem, queueingFunctionFlag):
    rootNode = Node(Problem.initialState)
    print("rootNode: " + str(rootNode.state))

    nodes = NodeQueue(rootNode)
    print("Queue: " + str(nodes.queue[0].state))

    expand(rootNode)
    
    # currNode = nodes.queue.pop()    
    # print("currNode: " + str(currNode.state))

    # print(len(nodes.queue))
    # while nodes:                                                            # While the queue of nodes is not empty
    #     currNode = nodes.queue.pop()                                        # Gets the top node off of the queue
    #     if Problem.goalTest(currNode):
    #         return currNode
    #     nodes = queueingFunction(nodes, expand(currNode, Problem.operators))    # need to add problem.operators but still confused
    # return Failure



Problem = Problem(A)
# endNode = generalSearch(Problem, "uniform")
generalSearch(Problem, "uniform")