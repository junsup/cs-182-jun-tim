from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

try:
  from search import SearchProblem
  from search import aStarSearch

except:
  from  CPF.search import SearchProblem
  from  CPF.search import aStarSearch

class PlanningProblem():
  def __init__(self, domain, problem):
    """
    Constructor
    """
    p = Parser(domain, problem)
    self.actions, self.propositions = p.parseActionsAndPropositions()	# list of all the actions and list of all the propositions
    self.initialState, self.goal = p.pasreProblem() 					# the initial state and the goal state are lists of propositions
    self.createNoOps() 													# creates noOps that are used to propagate existing propositions from one layer to the next
    PlanGraphLevel.setActions(self.actions)
    PlanGraphLevel.setProps(self.propositions)
    self._expanded = 0


  def getStartState(self):
    return self.initialState


  def isGoalState(self, state):
    return not self.goalStateNotInPropLayer(state)


  def getSuccessors(self, state):
    """
    For a given state, this should return a list of triples,
    (successor, action, stepCost), where 'successor' is a
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental
    cost of expanding to that successor
    Hint:  check out action.allPrecondsInList
    """
    self._expanded += 1
    actions = []
    for act in self.actions:
      if not act.isNoOp() and act.allPrecondsInList(state):
        actions.append(act)

    succs = []
    for act in actions:
      newState = copy.deepcopy(act.getAdd())
      for p in state:
        if p not in act.getDelete():
          newState.append(p)
      succs.append((newState, act, 1))

    return succs

  def getCostOfActions(self, actions):
    return len(actions)

  def goalStateNotInPropLayer(self, propositions):
    """
    Helper function that returns true if all the goal propositions
    are in propositions
    """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False

  def createNoOps(self):
    """
    Creates the noOps that are used to propagate propositions from one layer to the next
    """
    for prop in self.propositions:
      name = prop.name
      precon = []
      add = []
      precon.append(prop)
      add.append(prop)
      delete = []
      act = Action(name,precon,add,delete, True)
      self.actions.append(act)

def maxLevel(state, problem):
  """
  The heuristic value is the number of layers required to expand all goal propositions.
  If the goal is not reachable from the state your heuristic should return float('inf')
  """
  newPropositionLayer = PropositionLayer()
  [newPropositionLayer.addProposition(p) for p in state]

  newPlanGraphLevel = PlanGraphLevel()
  newPlanGraphLevel.setPropositionLayer(newPropositionLayer)

  level = 0
  g = [newPlanGraphLevel]

  while problem.goalStateNotInPropLayer(g[level].getPropositionLayer().getPropositions()):
    if isFixed(g, level):
      return float("inf")

    level += 1
    nextPlanGraphLevel = PlanGraphLevel()
    nextPlanGraphLevel.expandWithoutMutex(g[level - 1])
    g.append(newPlanGraphLevel)

  return level



def levelSum(state, problem):
  """
  The heuristic value is the sum of sub-goals level they first appeared.
  If the goal is not reachable from the state your heuristic should return float('inf')
  """
  total = 0
  propLayerInit = PropositionLayer()

  for prop in state:
    propLayerInit.addProposition(prop)

  pgInit = PlanGraphLevel()
  pgInit.setPropositionLayer(propLayerInit)
  g = [pgInit]
  level = 0

  while len(problem.goal) > 0:
    if isFixed(g, level):
      return float("inf")

    for goal in problem.goal:
      if goal in g[level].getPropositionLayer().getPropositions():
        problem.goal.remove(goal)
        total += level

    nextPlanGraphLevel = PlanGraphLevel()
    nextPlanGraphLevel.expandWithoutMutex(g[level])
    level += 1
    g.append(nextPlanGraphLevel)
  return total


def isFixed(Graph, level):
  """
  Checks if we have reached a fixed point,
  i.e. each level we'll expand would be the same, thus no point in continuing
  """
  if level == 0:
    return False

  if len(Graph[level].getPropositionLayer().getPropositions()) == len(Graph[level - 1].getPropositionLayer().getPropositions()):
    return True
  return False


if __name__ == '__main__':
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 4:
    print "Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)"
    exit()
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  heuristic = lambda x,y: 0
  if len(sys.argv) == 4:
    domain = str(sys.argv[1])
    problem = str(sys.argv[2])
    if str(sys.argv[3]) == 'max':
      heuristic = maxLevel
    elif str(sys.argv[3]) == 'sum':
      heuristic = levelSum
    elif str(sys.argv[3]) == 'zero':
      heuristic = lambda x,y: 0
    else:
      print "Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)"
      exit()

  prob = PlanningProblem(domain, problem)
  start = time.clock()
  plan = aStarSearch(prob, heuristic)
  elapsed = time.clock() - start
  if plan is not None:
    print "Plan found with %d actions in %.2f seconds" % (len(plan), elapsed)
  else:
    print "Could not find a plan in %.2f seconds" %  elapsed
  print "Search nodes expanded: %d" % prob._expanded

