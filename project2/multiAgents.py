# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util, sys  #added sys

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
    newFood = successorGameState.getFood()    #newFood.asList() gets you the LOCATIONS of the food where as this is booleans
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #TWO OVERALL GOALS: eat food, avoid ghosts

    #want to eat the closest food so the closer to food the better
    newFood = newFood.asList()
    closest_food = sys.maxint
    for food in newFood:
      food_dist = manhattanDistance(newPos, food)
      if(food_dist < closest_food):
        closest_food = food_dist

    #but need to avoid ghosts
    ghost_positions = successorGameState.getGhostPositions()
    for ghost in ghost_positions:
      if(manhattanDistance(newPos, ghost)<3):
        return -sys.maxint                       #REALLY BAD DO NOT PASS GO LET'S NOT GO HERE WE'RE TOO CLOSE

    #                                         reciprocal (from instructions) allows a close food to be a high score (which is what we want)
    return successorGameState.getScore() + 1.0/closest_food

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  #The pseudocode has 3 functions... function that calls min or max, the max function, the min function

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
    "*** YOUR CODE HERE ***"
    #Pacman is a max level so we will want to get the info from the function for max level
    return self.maxlevel(gameState, 0, 0)[1]     #THIS NEEDS TO BE AN ACTION
  
  def minimax(self, gameState, index, depth):
    #this would mean we are at a terminal node or the game is over
    if depth is self.depth * gameState.getNumAgents():
       return self.evaluationFunction(gameState)
    if gameState.isLose() or gameState.isWin():
        return self.evaluationFunction(gameState)

    #the root is pacman which is a maxlevel and index 0 so by pattern, even indicies will go to maxlevel and odd to minlvel
    if index == 0:
      return self.maxlevel(gameState, 0, depth)[0]
    else:
      return self.minlevel(gameState, index, depth)[0]
  
  def maxlevel(self, gameState, index, depth):
    #initiate to -inf
    v = [-sys.maxint, "action"]

    #for each successor of state
    legal_actions = gameState.getLegalActions(index)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))
    
    #take the max
    for successor in successors:
      succ_action = (self.minimax(successor[0], (depth + 1)%gameState.getNumAgents(), depth+1), successor[1])
      if(v[0]<succ_action[0]):
        v=succ_action
    
    return v
  
  def minlevel(self, gameState, index, depth):
    #initiate to inf
    v = [sys.maxint, "action"]

    #for each successor of state
    legal_actions = gameState.getLegalActions(index)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))
    
    #take the min
    for successor in successors:
      succ_action = (self.minimax(successor[0], (depth + 1)%gameState.getNumAgents(), depth+1), successor[1])
      #if(v[0]<succ_action[0]):
        #v=succ_action
      if(succ_action[0]<v[0]):
        v=succ_action
    
    return v

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  #Going to be structurally similar to minimax

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    #Pacman is a max level so we will want to get the info from the function for max level
    action = self.maxlevel(gameState, 0, 0, -sys.maxint, sys.maxint)[1]
    #print action
    return action
  
  def alphabeta(self, gameState, index, depth, alpha, beta):
    #this would mean we are at a terminal node or the game is over
    if depth is self.depth * gameState.getNumAgents():
       return self.evaluationFunction(gameState)
    if gameState.isLose() or gameState.isWin():
        return self.evaluationFunction(gameState)

    #the root is pacman which is a maxlevel and index 0 so by pattern, even indicies will go to maxlevel and odd to minlvel
    if index == 0:
      return self.maxlevel(gameState, 0, depth, alpha, beta)[0]
    else:
      return self.minlevel(gameState, index, depth, alpha, beta)[0]

  def maxlevel(self, gameState, index, depth, alpha, beta):
    #initiate to -inf
    v = [-sys.maxint, "action"]

    #for each successor of state
    legal_actions = gameState.getLegalActions(index)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))
    
    #take the max
    for successor in successors:
      succ_action = (self.alphabeta(successor[0], (depth + 1)%gameState.getNumAgents(), depth+1, alpha, beta), successor[1])
      if(v[0]<succ_action[0]):
        v=succ_action
      #here is the pruning
      if(v[0] > beta):
        return v
      else: alpha = max(v[0], alpha)
      
    return v

  def minlevel(self, gameState, index, depth, alpha, beta):
    #initiate to inf
    v = [sys.maxint, "action"]

    #for each successor of state
    legal_actions = gameState.getLegalActions(index)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))
    
    #take the min
    for successor in successors:
      succ_action = (self.alphabeta(successor[0], (depth + 1)%gameState.getNumAgents(), depth+1, alpha, beta), successor[1])
      if(succ_action[0]<v[0]):
        v=succ_action
      #here is the pruning
      if(v[0] < alpha):
        return v
      else: beta = min(v[0], beta)
      
    return v

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  #will be similar function structure to the last two

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    #Pacman is a max level so we will want to get the info from the function for max level
    return self.maxlevel(gameState, 0, 0, "action")[1]     #THIS NEEDS TO BE AN ACTION
  
  def expectimax(self, gameState, index, depth, action):
    #this would mean we are at a terminal node or the game is over
    if depth is self.depth * gameState.getNumAgents():
       return self.evaluationFunction(gameState)
    if gameState.isLose() or gameState.isWin():
        return self.evaluationFunction(gameState)

    #the root is pacman which is a maxlevel and index 0 so by pattern, even indicies will go to maxlevel and odd to minlvel
    if index == 0:
      return self.maxlevel(gameState, 0, depth, action)[0]
    else:
      return self.explevel(gameState, index, depth, action)[0]
  
  def maxlevel(self, gameState, index, depth, action):
    #initiate to -inf
    v = [-sys.maxint, "action"]

    #for each successor of state
    legal_actions = gameState.getLegalActions(index)
    if not legal_actions:
      return self.evaluationFunction(gameState)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))
    
    #take the max
    for successor in successors:
      succ_action = (self.expectimax(successor[0], (depth + 1)%gameState.getNumAgents(), depth+1, successor[1]), successor[1])
      if(v[0]<succ_action[0]):
        v=succ_action
    
    return v
  
  def explevel(self, gameState, index, depth, action):
    #initiate to 0
    v = [0, "action"]

    #for each successor of state
    legal_actions = gameState.getLegalActions(index)
    if not legal_actions:
      return self.evaluationFunction(gameState)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))

    #find the probability
    prob = 1/len(legal_actions)
    for successor in successors:
      v[0] += prob * self.expectimax(successor[0], (depth + 1)%gameState.getNumAgents(), depth+1, action)
    
    return v



def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I pulled in and calculated values about the current state which affect its value, then weighted each piece of
    information based on its importance to the state's value.
  """
  "*** YOUR CODE HERE ***"

  if currentGameState.isLose():
    return -sys.maxint
  elif currentGameState.isWin():
    return sys.maxint

  #useful values
  pac_pos = currentGameState.getPacmanPosition()
  food_pos = currentGameState.getFood().asList()
  ghost_pos = currentGameState.getGhostPositions()
  cap_pos = currentGameState.getCapsules()
  ghosts = currentGameState.getGhostStates()

  #check if food is nearby
  closest_food = sys.maxint
  for food in food_pos:
    food_dist = abs(pac_pos[0]-food[0]) + abs(pac_pos[1]-food[1])
    #update closest food
    if (food_dist < closest_food):
      closest_food = food_dist

  #check if ghosts are nearby
  close_ghost = sys.maxint
  for ghost in ghost_pos:
      ghost_dist = abs(pac_pos[0]-ghost[0]) + abs(pac_pos[1]-ghost[1])
      #update closest ghost
      if (ghost_dist < close_ghost):
        close_ghost = ghost_dist

  # #check if capsule is nearby
  closest_capsule = sys.maxint
  for capsule in cap_pos:
    cap_dist = abs(pac_pos[0]-capsule[0]) + abs(pac_pos[1]-capsule[1])
    #update closest capsule
    if (cap_dist < closest_capsule):
      closest_capsule = cap_dist

   #check if any ghosts are scared
  scared_time = 0
  for ghost in ghosts:
    if scared_time < ghost.scaredTimer:
      scared_time = ghost.scaredTimer

  #generate the scores (closest food, closest ghost, amount of food, closest capsule, scared timer)

  #closest food
  if closest_food == 0:
    food_score = 1000000
  else:
    food_score = 1.0/closest_food

  #closest ghost
  if scared_time > 2:
    ghost_score = 1.0/ghost_dist
  elif ghost_dist < 3:
    ghost_score = -10000000
  else:
    ghost_score = ghost_dist

  # amt food
  num_food_left = currentGameState.getNumFood()
  foodnum_score = 100/num_food_left

  #closest capsule
  cap_score = 1000/closest_capsule

  #num capsules
  capnum_score = 0
  if len(cap_pos) != 0:
    capnum_score = 100000/len(cap_pos)

  # #scared timer
  scare_score = 0
  if scared_time > 2:
    scare_score = 100000

  #combine scores and return
  eval = 1000000*currentGameState.getScore() + foodnum_score + cap_score + capnum_score + scare_score + ghost_score + food_score
  return eval





# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
    Description: I combined the Minimax implementation to account for the ghosts behaving (somewhat)
    rationally and my better eval function which deals well with the capsules/scared ghosts.
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    return self.maxlevel(gameState, 0, 0)[1]

  def minimax(self, gameState, index, depth):
    # this would mean we are at a terminal node or the game is over
    if depth is self.depth * gameState.getNumAgents():
      return betterEvaluationFunction(gameState)
    if gameState.isLose() or gameState.isWin():
      return betterEvaluationFunction(gameState)

  # the root is pacman which is a maxlevel and index 0 so by pattern, even indicies will go to maxlevel and odd to minlvel
    if index == 0 % 2:
      return self.maxlevel(gameState, 0, depth)[0]
    else:
      return self.minlevel(gameState, index, depth)[0]


  def maxlevel(self, gameState, index, depth):
    # initiate to -inf
    v = [-sys.maxint, "action"]

    # for each successor of state
    legal_actions = gameState.getLegalActions(index)
    if not legal_actions:
      return self.evaluationFunction(gameState)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))

    # take the max
    for successor in successors:
      succ_action = (self.minimax(successor[0], (depth + 1) % gameState.getNumAgents(), depth + 1), successor[1])
      if (v[0] < succ_action[0]):
        v = succ_action

    return v


  def minlevel(self, gameState, index, depth):
    # initiate to inf
    v = [sys.maxint, "action"]

    # for each successor of state
    legal_actions = gameState.getLegalActions(index)
    if not legal_actions:
      return self.evaluationFunction(gameState)
    successors = list()
    for action in legal_actions:
      successors.append((gameState.generateSuccessor(index, action), action))

  # take the min
    for successor in successors:
      succ_action = (self.minimax(successor[0], (depth + 1) % gameState.getNumAgents(), depth + 1), successor[1])
      # if(v[0]<succ_action[0]):
      # v=succ_action
      if (succ_action[0] < v[0]):
        v = succ_action

    return v



