# Jun Lee, Tim McLaughlin
# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newGhostPositions = successorGameState.getGhostPositions()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # calculates manhattan distance to closest food
    try:
      foodDist = min([manhattanDistance(newPos, x)
        for x in newFood.asList()])
    except ValueError:
      foodDist = 0
    foodScore = 1.0 / (foodDist + 0.01)

    # calculates manhattan distance to closest ghost
    ghostDist = min([manhattanDistance(newPos, x.getPosition())
      for x in newGhostStates])
    ghostScore = -1.0 / (ghostDist + 0.001)

    return successorGameState.getScore() + ghostScore +  foodScore

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    return self.getMax(gameState)[0]

  def getMax(self, gameState, depth=1):
    legalMoves = gameState.getLegalPacmanActions()
    # Default initialization of return values
    maxEval = -float("inf")
    # There can be multiple moves that share maxEval
    maxMoves = set([Directions.STOP])

    for move in legalMoves:
      successorState = gameState.generatePacmanSuccessor(move)
      successorEval = self.getMin(successorState, 1, depth)
      if successorEval > maxEval:
        maxMoves = set([move])
        maxEval = successorEval
      elif successorEval == maxEval:
        maxMoves.add(move)
    # Avoid not moving unless it has the absolute max utility
    if len(maxMoves) > 1 and Directions.STOP in maxMoves:
      maxMoves.remove(Directions.STOP)
    return random.choice(list(maxMoves)), maxEval

  def getMin(self, gameState, agentIndex, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    legalMoves = gameState.getLegalActions(agentIndex)
    # Default initialization of return value
    evals = []
    # If last ghost, increment depth
    if agentIndex == gameState.getNumAgents() - 1:
      if depth == self.depth:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          successorEval = self.evaluationFunction(successorState)
          evals.append(successorEval)
      else:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          evals.append(self.getMax(successorState, depth + 1)[1])
    else:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          evals.append(self.getMin(successorState, agentIndex + 1, depth))
    if evals:
      return min(evals)
    return float("inf")

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    # print self.getMax(gameState, 1, -float("inf"), float("inf"))[1]
    return self.getMax(gameState, 1, -float("inf"), float("inf"))[0]

  def getMax(self, gameState, depth, alpha, beta):
    legalMoves = gameState.getLegalPacmanActions()
    # Default initialization of return values
    maxEval = -float("inf")
    # There can be multiple moves that share maxEval
    maxMoves = set([Directions.STOP])

    for move in legalMoves:
      successorState = gameState.generatePacmanSuccessor(move)
      successorEval = self.getMin(successorState, 1, depth, alpha, beta)
      if successorEval > maxEval:
        maxMoves = set([move])
        maxEval = successorEval
      elif successorEval == maxEval:
        maxMoves.add(move)
      # Alpha beta pruning
      if maxEval >= beta:
        # Avoid not moving unless it has the absolute max utility
        if len(maxMoves) > 1 and Directions.STOP in maxMoves:
          maxMoves.remove(Directions.STOP)
        return random.choice(list(maxMoves)), maxEval
      alpha = max(alpha, maxEval)
    # Avoid not moving unless it has the absolute max utility
    if len(maxMoves) > 1 and Directions.STOP in maxMoves:
      maxMoves.remove(Directions.STOP)
    return random.choice(list(maxMoves)), maxEval

  def getMin(self, gameState, agentIndex, depth, alpha, beta):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    legalMoves = gameState.getLegalActions(agentIndex)
    # Default initialization of return value
    evals = []
    # If last ghost, increment depth
    if agentIndex == gameState.getNumAgents() - 1:
      if depth == self.depth:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          successorEval = self.evaluationFunction(successorState)
          evals.append(successorEval)
        # Alpha beta pruning
        if successorEval <= alpha:
          return successorEval
        beta = min(beta, successorEval)
      else:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          successorEval = self.getMax(successorState, depth + 1, alpha, beta)[1]
          evals.append(successorEval)
        # Alpha beta pruning
        if successorEval <= alpha:
          return successorEval
        beta = min(beta, successorEval)
    else:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          successorEval = self.getMin(successorState, agentIndex + 1, depth, alpha, beta)
          evals.append(successorEval)
        # Alpha beta pruning
        if successorEval <= alpha:
          return successorEval
        beta = min(beta, successorEval)
    if evals:
      return min(evals)
    return float("inf")

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    return self.getMax(gameState)[0]

  def getMax(self, gameState, depth=0):
    legalMoves = gameState.getLegalPacmanActions()
    # Default initialization of return values
    maxEval = -float("inf")
    # There can be multiple moves that share maxEval
    maxMoves = set([Directions.STOP])

    for move in legalMoves:
      successorState = gameState.generatePacmanSuccessor(move)
      successorEval = self.getExpected(successorState, 1, depth)
      if successorEval > maxEval:
        maxMoves = set([move])
        maxEval = successorEval
      elif successorEval == maxEval:
        maxMoves.add(move)
    # Avoid not moving unless it has the absolute max utility
    if len(maxMoves) > 1 and Directions.STOP in maxMoves:
      maxMoves.remove(Directions.STOP)
    return random.choice(list(maxMoves)), maxEval

  def getExpected(self, gameState, agentIndex, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    legalMoves = gameState.getLegalActions(agentIndex)
    # Default initialization of return value
    evals = []
    # If last ghost, increment depth
    if agentIndex == gameState.getNumAgents() - 1:
      if depth == self.depth:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          successorEval = self.evaluationFunction(successorState)
          evals.append(successorEval)
      else:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          evals.append(self.getMax(successorState, depth + 1)[1])
    else:
        for move in legalMoves:
          successorState = gameState.generateSuccessor(agentIndex, move)
          evals.append(self.getExpected(successorState, agentIndex + 1, depth))
    # Return expected value of evals with naive probability
    if evals:
      return sum(evals)/len(evals)
    return float(0)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """

  if currentGameState.isLose():
    return float("-inf")
  elif currentGameState.isWin():
    return float("inf")

  curPos = currentGameState.getPacmanPosition()
  # food evaluations
  foodPositions = currentGameState.getFood().asList()
  nFood = len(foodPositions)
  if nFood is 0:
    foodEval = 0
  else:
    foodDist = [manhattanDistance(curPos, x) for x in foodPositions]
    averageFoodDist = float(sum(foodDist)) / nFood
    foodEval = 1.0 / (nFood + averageFoodDist)

  capsulePositions = currentGameState.getCapsules()
  nCapsules = len(capsulePositions)
  if nCapsules is 0:
    capsuleEval = 0
  else:
    capsuleDist = [manhattanDistance(curPos, x) for x in foodPositions]
    averageCapsuleDist = float(sum(capsuleDist)) / nCapsules
    capsuleEval = 4.0 / (nCapsules + averageCapsuleDist)

  # ghost evaluation
  ghostEval = 0
  for ghostPos in currentGameState.getGhostPositions():
    ghostEval += 1.0 / (manhattanDistance(curPos, ghostPos) + .001) ** 2


  # print currentGameState.getNumFood()
  result = foodEval + capsuleEval + ghostEval + currentGameState.getScore()
  return result

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

