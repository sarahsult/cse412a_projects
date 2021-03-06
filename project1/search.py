# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    
    tree = util.Stack()
    start = problem.getStartState()
    if(problem.isGoalState(start)):
        return []
    tree.push((start, []))  #the empty vector will hold the path from start to node (but there doesn't exist one for start)
    expanded_nodes = []
    
    while not tree.isEmpty():
        current, moves = tree.pop() 
        if current not in expanded_nodes:
            expanded_nodes.append(current)

            if problem.isGoalState(current):
                return moves
            
            successors = problem.getSuccessors(current)
            #for every successor
            for i in range(0,len(successors)):
                path = moves + [successors[i][1]]
                tree.push((successors[i][0], path))
    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"

    #This will be the same as DFS but changing the data structure for the tree changes what nodes are popped and allows for 
    #breath vs depth
    tree = util.Queue()
    start = problem.getStartState()
    if(problem.isGoalState(start)):
        return []
    tree.push((start, []))  
    expanded_nodes = []
    
    while not tree.isEmpty():
        current, moves = tree.pop() 
        if current not in expanded_nodes:
            expanded_nodes.append(current)

            if problem.isGoalState(current):
                return moves
            
            successors = problem.getSuccessors(current)
            #for every successor
            for i in range(0,len(successors)):
                path = moves + [successors[i][1]]
                tree.push((successors[i][0], path))


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    tree = util.PriorityQueue()
    start = problem.getStartState()
    if(problem.isGoalState(start)):
        return []
    tree.push((start, [], 0), 0)  #the empty vector will hold the path from start to node (but there doesn't exist one for 
    #               start and the 0 is going to be the priority which corresponds to the cost to get to that node; you need both
    #               values because one tell in what order to pop from but you need to be able to access that value after popping
    #               so it has to go in with the node info
    expanded_nodes = []

    while not tree.isEmpty():
        current, moves, cost = tree.pop()
        if current not in expanded_nodes:
            expanded_nodes.append(current)
        
            if problem.isGoalState(current):
                return moves
            
            successors = problem.getSuccessors(current)
            #for every successor
            for i in range(0,len(successors)):
                path = moves + [successors[i][1]]
                newcost = cost + successors[i][2]
                tree.push((successors[i][0], path, newcost), newcost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    #This can be the same as UCS but changing what the priority is in the priority queue
    tree = util.PriorityQueue()
    start = problem.getStartState()
    if(problem.isGoalState(start)):
        return []
    tree.push((start, [], 0), 0)  
    expanded_nodes = []

    while not tree.isEmpty():
        current, moves, cost = tree.pop()
        if current not in expanded_nodes:
            expanded_nodes.append(current)
        
            if problem.isGoalState(current):
                return moves
            
            successors = problem.getSuccessors(current)
            #for every successor
            for i in range(0,len(successors)):
                path = moves + [successors[i][1]]
                gn = cost + successors[i][2] 
                hn = heuristic(successors[i][0], problem)
                tree.push((successors[i][0], path, gn), (gn+hn))

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
