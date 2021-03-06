"""
Created on Oct 20, 2013

@author: Ofra
"""
from action import Action
from actionLayer import ActionLayer
from util import Pair
from proposition import Proposition
from propositionLayer import PropositionLayer

class PlanGraphLevel(object):
  """
  A class for representing a level in the plan graph.
  For each level i, the PlanGraphLevel consists of the actionLayer and propositionLayer at this level in this order!
  """
  independentActions = []  # updated to the independentActions of the propblem GraphPlan.py line 31
  actions = []             # updated to the actions of the problem GraphPlan.py line 32 and planningProblem.py line 25
  props = []               # updated to the propositions of the problem GraphPlan.py line 33 and planningProblem.py line 26

  @staticmethod
  def setIndependentActions(independentActions):
    PlanGraphLevel.independentActions = independentActions

  @staticmethod
  def setActions(actions):
    PlanGraphLevel.actions = actions

  @staticmethod
  def setProps(props):
    PlanGraphLevel.props = props

  def __init__(self):
    """
    Constructor
    """
    self.actionLayer = ActionLayer()    		# see actionLayer.py
    self.propositionLayer = PropositionLayer()	# see propositionLayer.py


  def getPropositionLayer(self):
    return self.propositionLayer

  def setPropositionLayer(self, propLayer):
    self.propositionLayer = propLayer

  def getActionLayer(self):
    return self.actionLayer

  def setActionLayer(self, actionLayer):
    self.actionLayer = actionLayer

  def updateActionLayer(self, previousPropositionLayer):
    """
    Updates the action layer given the previous proposition layer (see propositionLayer.py)
    allAction is the list of all the action (include noOp in the domain)
    """
    allActions = PlanGraphLevel.actions
    for action in allActions:
      if previousPropositionLayer.allPrecondsInLayer(action):
        self.actionLayer.addAction(action)
        for p1 in action.getPre():
          for p2 in action.getPre():
            if previousPropositionLayer.isMutex(p1, p2):
              self.actionLayer.removeActions(action)

  def updateMutexActions(self, previousLayerMutexProposition):
    """
    Updates the mutex list in self.actionLayer,
    given the mutex proposition from the previous layer.
    currentLayerActions are the actions in the current action layer
    """
    currentLayerActions = self.actionLayer.getActions()
    for a1 in currentLayerActions:
      for a2 in currentLayerActions:
        if a1 == a2:
          continue
        if mutexActions(a1, a2, previousLayerMutexProposition):
          self.actionLayer.addMutexActions(a1, a2)


  def updatePropositionLayer(self):
    """
    Updates the propositions in the current proposition layer,
    given the current action layer.
    don't forget to update the producers list!
    """
    currentLayerActions = self.actionLayer.getActions()
    propsToAdd = dict()
    for action in currentLayerActions:
      for prop in action.getAdd():
        if prop.getName() not in propsToAdd:
          propsToAdd[prop.getName()] = Proposition(prop.getName())
        temp = propsToAdd[prop.getName()]
        if action not in temp.getProducers():
          temp.addProducer(action)
    for prop in propsToAdd.values():
      self.propositionLayer.addProposition(prop)

  def updateMutexProposition(self):
    """
    updates the mutex propositions in the current proposition layer
    """
    currentLayerPropositions = self.propositionLayer.getPropositions()
    currentLayerMutexActions =  self.actionLayer.getMutexActions()
    for prop1 in currentLayerPropositions:
      for prop2 in currentLayerPropositions:
        if prop1 == prop2:
          continue
        if mutexPropositions(prop1, prop2, currentLayerMutexActions):
          self.propositionLayer.addMutexProp(prop1, prop2)


  def expand(self, previousLayer):
    """
    Your algorithm should work as follows:
    First, given the propositions and the list of mutex propositions from the previous layer,
    set the actions in the action layer.
    Then, set the mutex action in the action layer.
    Finally, given all the actions in the current layer, set the propositions and their mutex relations in the proposition layer.
    """
    previousPropositionLayer = previousLayer.getPropositionLayer()
    previousLayerMutexProposition = previousPropositionLayer.getMutexProps()

    self.updateActionLayer(previousPropositionLayer)
    self.updateMutexActions(previousLayerMutexProposition)
    self.updatePropositionLayer()
    self.updateMutexProposition()


  def expandWithoutMutex(self, previousLayer):
    """
    Questions 11 and 12
    You don't have to use this function
    """
    previousLayerProposition = previousLayer.getPropositionLayer()
    "*** YOUR CODE HERE ***"


def mutexActions(a1, a2, mutexProps):
  """
  Complete code for deciding whether actions a1 and a2 are mutex,
  given the mutex proposition from previous level (list of pairs of propositions).
  Your updateMutexActions function should call this function
  """
  if Pair(a1, a2) not in PlanGraphLevel.independentActions:
      return True

  for x in [Pair(y, z) for y in a1.getPre() for z in a2.getPre()]:
    if x in mutexProps:
        return True
  return False


def mutexPropositions(prop1, prop2, mutexActions):
  """
  complete code for deciding whether two propositions are mutex,
  given the mutex action from the current level (list of pairs of actions).
  Your updateMutexProposition function should call this function
  """
  for a1 in prop1.getProducers():
    for a2 in prop2.getProducers():
      if Pair(a1, a2) not in mutexActions:
        return False
  return True
