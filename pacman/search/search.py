# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]
    

def depthFirstSearch(problem):
	# for DFS, Stack is used                      
	fringe_stack = util.Stack()
	closed = set()	# Visited Nodes
	direction =[]	# Path
	push_pair = (problem.getStartState(),direction)
	fringe_stack.push(push_pair)
	while True:
		if fringe_stack.isEmpty():
			break

		popped = fringe_stack.pop()

		if problem.isGoalState(popped[0]):
			return popped[1]
		
		if not popped[0] in closed:
			closed.add(popped[0])
        
		for node,act,y in problem.getSuccessors(popped[0]):
			if node not in closed:
				direction = popped[1] + [act]
				push_pair = (node,direction)
				fringe_stack.push(push_pair)
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.
    """
	
# ________________________________________________________________

class _RecursiveDepthFirstSearch(object):
    def __init__(self, problem):
        "Do not change this." 
        # You'll save the actions that recursive dfs found in self.actions. 
        self.actions = [] 
        # Use self.explored to keep track of explored nodes.  
        self.explored = set()
        self.problem = problem

    def RecursiveDepthFirstSearchHelper(self, node):
        if not node in self.explored:
            self.explored.add(node)
        
            # Returns true if goal is found
            if self.problem.isGoalState(node):
                return True
        
            else:
                # Get childnodes and reverse (only in case of recursion not iteration)
                child_nodes = self.problem.getSuccessors(node)
                child_nodes.reverse()
                for nodes,action,y in child_nodes:
                    result = self.RecursiveDepthFirstSearchHelper(nodes)
                    # Add to path if goal is found (helper function returns true)
                    if (result == True): 
                        self.actions.append(action)
                        return True
                
          
def RecursiveDepthFirstSearch(problem):
    " You need not change this function. "
    # All your code should be in member function 'RecursiveDepthFirstSearchHelper' of 
    # class '_RecursiveDepthFirstSearch'."

    node = problem.getStartState() 
    rdfs = _RecursiveDepthFirstSearch(problem)
    path_found = rdfs.RecursiveDepthFirstSearchHelper(node)
    return list(reversed(rdfs.actions)) # Actions your recursive calls return are in opposite order.
# ________________________________________________________________


def depthLimitedSearch(problem, limit = 129):
    fringe_stack = util.Stack()
    closed = set()	# Visited Nodes
    direction =[]	# Path
    depth = 0
                                    
    push_tuple = (problem.getStartState(),direction,depth)
    fringe_stack.push(push_tuple)
    while True:
        if fringe_stack.isEmpty():
            break
        
        popped = fringe_stack.pop()
        
        if (limit == 0):
            return False

        
        if ((popped[2] > limit) and problem.isGoalState(popped[0])):
            return popped[1]

        if not popped[0] in closed:
            current_depth = popped[2] + 1
            closed.add(popped[0])
            
        
        for node,act,y in problem.getSuccessors(popped[0]):
            if node not in closed:
                direction = popped[1] + [act]
                push_tuple = (node,direction,current_depth)
                fringe_stack.push(push_tuple)
            
            
              
 # ________________________________________________________________

class _RecursiveDepthLimitedSearch(object):
    '''
        => Output of 'recursive' dfs should match that of 'iterative' dfs you implemented
        above. 
        Key Point: Remember in tutorial you were asked to expand the left-most child 
        first for dfs and bfs for consistency. If you expanded the right-most
        first, dfs/bfs would be correct in principle but may not return the same
        path. 

        => Useful Hint: self.problem.getSuccessors(node) will return children of 
        a node in a certain "sequence", say (A->B->C), If your 'recursive' dfs traversal 
        is different from 'iterative' traversal, try reversing the sequence.  

    '''
    def __init__(self, problem):
        " Do not change this. " 
        # You'll save the actions that recursive dfs found in self.actions. 
        self.actions = [] 
        # Use self.explored to keep track of explored nodes.  
        self.explored = set()
        self.problem = problem
        self.current_depth = 0
        self.depth_limit = 204 # For medium maze, You should find solution for depth_limit not more than 204.

    def RecursiveDepthLimitedSearchHelper(self, node):
        if not node in self.explored:
            self.explored.add(node)
        
            # Returns true if goal is found and limit condition is satisfied
            if (self.problem.isGoalState(node) and (self.depth_limit >= self.current_depth)):
                return True
        
            else:
                # Get childnodes and reverse (only in case of recursion not iteration)
                child_nodes = self.problem.getSuccessors(node)
                child_nodes.reverse()
                for nodes,action,y in child_nodes:
                    result = self.RecursiveDepthLimitedSearchHelper(nodes)
                    # Add to path if goal is found (helper function returns true)
                    if result: 
                        self.actions.append(action)
                        self.current_depth = self.current_depth + 1
                        return True


def RecursiveDepthLimitedSearch(problem):
	"You need not change this function. All your code in member function RecursiveDepthLimitedSearchHelper"
	node = problem.getStartState() 
	rdfs = _RecursiveDepthLimitedSearch(problem)
	path_found = rdfs.RecursiveDepthLimitedSearchHelper(node)
	return list(reversed(rdfs.actions)) # Actions your recursive calls return are in opposite order.
# ________________________________________________________________


def breadthFirstSearch(problem):
	# For BFS, Queue is used
	fringe_queue = util.Queue()
	closed = set()		# Visited Nodes
	direction =[]		# Path (Entire path will be returned in the end)
	push_pair = (problem.getStartState(),direction)
	fringe_queue.push(push_pair)
	while True:
		# Continue loop till Queue is empty
		# i.e All nodes have been covered
		if fringe_queue.isEmpty():
			break

		popped = fringe_queue.pop()

		# Return if Goal is found
		if problem.isGoalState(popped[0]):
			return popped[1]
		
		if not popped[0] in closed:
			closed.add(popped[0])
        
		for node,act,y in problem.getSuccessors(popped[0]):
			if node not in closed:
				closed.add(node)
				direction = popped[1] + [act]
				push_pair = (node,direction)
				fringe_queue.push(push_pair)


def uniformCostSearch(problem):
	fringe_pqueue = util.PriorityQueue()
	closed = []
	direction =[]
	cost = 0
	push_tuple = (problem.getStartState(),direction,cost)
	fringe_pqueue.push(push_tuple,cost)
	while True:
		if fringe_pqueue.isEmpty():
			break
		
		popped,costs = fringe_pqueue.pop()

		if problem.isGoalState(popped[0]):
			return popped[1]
		
		if not popped[0] in closed:
			closed.append(popped[0])
        
			for node,act,each_cost in problem.getSuccessors(popped[0]):
				cost = popped[2] + each_cost
				direction = popped[1] + [act]
				push_tuple = (node,direction,cost)
				fringe_pqueue.push(push_tuple,cost)
	

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	'''
	Pay clos attention to util.py- specifically, args you pass to member functions. 

	Key Point: If a node is already present in the queue with higher path cost, 
	you'll update its cost (Similar to pseudocode in figure 3.14 of your textbook.). Be careful, 
	autograder cannot catch this bug.

	'''
	fringe_pqueue = util.PriorityQueue()
	closed = []		# Visited Nodes
	direction =[]	# Path
	cost = 0
	push_tuple = (problem.getStartState(),direction,cost)
	fringe_pqueue.push(push_tuple,cost)
	while True:
		# Continue loop till queue is empty
		if fringe_pqueue.isEmpty():
			break
		
		popped,costs = fringe_pqueue.pop()

		# Return path if goal state is found
		if problem.isGoalState(popped[0]):
			return popped[1]
		
		if not popped[0] in closed:
			closed.append(popped[0])
        
			for node,act,each_cost in problem.getSuccessors(popped[0]):
				cost = popped[2] + each_cost
				hcost = cost + heuristic(node,problem)
				direction = popped[1] + [act]
				push_tuple = (node,direction,cost)
				fringe_pqueue.push(push_tuple,hcost)
		
		

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
rdfs = RecursiveDepthFirstSearch
dls = depthLimitedSearch
rdls = RecursiveDepthLimitedSearch
astar = aStarSearch
ucs = uniformCostSearch
