# CS170Project1

## General (Generic) Search Algorithm

    function general-search(problem, QUEUEING-FUNCTION)
    nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
  
    loop do
        if EMPTY(nodes) then return "Failure" # We have proved there is no solution  
        node = REMOVE-FRONT(nodes) 
        if problem.GOAL-TEST(node.STATE) succeeds then return node 
        nodes = QUEUEING-FUNCTION(nodes,EXPAND(node,problem.OPERATORS))  
    end loop


### Explanation
GOAL-TEST(node.STATE) - This tests looks at a node/state and asks if this has reached the goal state

QUEUEING-FUNCTION - enqueues nodes in a certain method, for example FIFO/Breadth-first search