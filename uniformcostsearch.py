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

  def printBoard(self):
    for j in range(3): # for every row in board
        print(str(self.initialState[j][0]) + ' ' + str(self.initialState[j][1]) + ' ' + str(self.initialState[j][2]))

Problem1 = Problem(A)
Problem1.printBoard()
# Board2 = Problem(B)
# Board2.printBoard()

class Node:
    def __init__(self, initialState):
        self.state = initialState
    
    # def makeNode(self):




def generalSearch(Problem1, queueingFunction):
    rootNode = Node(Problem.initialState)
    nodes = makeQueue(makeNode(problem.initialState))

    while nodes:
        node = nodes.pop()
        if (node == checkGoalState(node.state)):
            return node
        nodes = queueingFunction(nodes, expand(node)) # need to add problem.operators but still confused
    return Failure