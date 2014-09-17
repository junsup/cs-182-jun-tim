import util
## Abstract Search Classes

class SearchProblem:
  """
  Abstract SearchProblem class. Your classes
  should inherit from this class and override 
  all the methods below
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
  """Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze"""
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

class Node:
  def __init__ (self, state, parent, action, cost):
    self.state = state
    self.parent = parent
    self.action = action
    self.cost = cost

  def expand (self, problem):
    successors = []
    for successor_state, action, cost in problem.getSuccessors(self.state):
      successors.append(Node(successor_state, self, action, self.cost + cost))
    return successors

def treeSearch(problem, fringe):
  visited_states = set()
  fringe.push(Node(problem.getStartState(), None, None, 0))
  while not fringe.isEmpty():
    current_node = fringe.pop()
    if problem.isGoalState(current_node.state):
      actions = []
      while (current_node.action is not None):
        actions.append(current_node.action)
        current_node = current_node.parent
      actions.reverse()
      return actions
    if current_node.state not in visited_states:
      visited_states.add(current_node.state)
      for successor in current_node.expand(problem):
        fringe.push(successor)
  return []

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first. [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  
  """
  "*** YOUR CODE HERE ***"
  return treeSearch(problem, util.Stack())

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  "*** YOUR CODE HERE ***"
  return treeSearch(problem, util.Queue())
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided searchProblem.  This one is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
def greedySearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()


