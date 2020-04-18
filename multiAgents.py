# multiAgents.py
# --------------
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldScore = currentGameState.getScore()
        newScore = successorGameState.getScore()
        scary = max(20, newScore - oldScore)

        minusFoodScore = len(newFood)
        if newScore < oldScore:
            minusFoodScore += min(manhattanDistance(newPos, food) for food in newFood)
        
        ghostPos = [ghost.getPosition() for ghost in newGhostStates]
        advantage = []
        for i in range(len(newGhostStates)):
            distance = manhattanDistance(newPos, ghostPos[i])
            if newScaredTimes[i] > 0:
                if newScaredTimes[i] > distance:
                    advantage.append(-5 * distance)
                else:
                    advantage.append(-0.5 * distance)
            else:
                if distance == 0:
                    return float('-inf')
                elif distance == 1:
                    advantage.append(len(newFood) * scary * 5)
                elif distance == 2:
                    advantage.append(len(newFood) * scary)
                else:
                    advantage.append(0)
        
        minusGhostScore = max(advantage)

        randomScore = random.uniform(0, 5)

        return newScore - minusFoodScore - minusGhostScore + randomScore
        
        # return successorGameState.getScore()

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

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        _, action = self.minimax(gameState, 1, 0)
        # print 'minimax value', _
        return action

    def minimax(self, gameState, depth, agentIndex):
        numAgents = gameState.getNumAgents()
        if depth == self.depth and agentIndex == numAgents - 1:
            return self.evaluationFunction(gameState), ''
        legalActions = gameState.getLegalActions(agentIndex)
        if len(legalActions) == 0:
            return self.evaluationFunction(gameState), ''
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
        if agentIndex == self.index:
            scores = [self.minimax(suc, depth, agentIndex + 1)[0] for suc in successorStates]
            result = max(scores)
            return result, legalActions[scores.index(result)]
        elif agentIndex == numAgents - 1:
            scores = [self.minimax(suc, depth + 1, self.index)[0] for suc in successorStates]
            result = min(scores)
            return result, legalActions[scores.index(result)]
        else:
            scores = [self.minimax(suc, depth, agentIndex + 1)[0] for suc in successorStates]
            result = min(scores)
            return result, legalActions[scores.index(result)]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = float('-inf'), ''
        b = float('inf'), ''
        _, action = self.alphabeta(gameState, 1, 0, a, b)
        # print 'alphabeta value', _
        return action

    def alphabeta(self, gameState, depth, agentIndex, a, b):
        numAgents = gameState.getNumAgents()
        if depth == self.depth and agentIndex == numAgents - 1:
            return self.evaluationFunction(gameState), ''
        legalActions = gameState.getLegalActions(agentIndex)
        if len(legalActions) == 0:
            return self.evaluationFunction(gameState), ''
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
        
        if agentIndex == self.index:
            v = float('-inf'), ''
            for i in range(len(successorStates)):
                t = self.alphabeta(successorStates[i], depth, agentIndex + 1, a, b)
                if t >= v: v = t[0], legalActions[i]
                if v >= b: return v
                if v > a: a = v
            return v
        elif agentIndex == numAgents - 1:
            v = float('inf'), ''
            for i in range(len(successorStates)):
                t = self.alphabeta(successorStates[i], depth + 1, self.index, a, b)
                if t <= v: v = t[0], legalActions[i]
                if a >= v: return v
                if b > v: b = v
            return v
        else:
            v = float('inf'), ''
            for i in range(len(successorStates)):
                t = self.alphabeta(successorStates[i], depth, agentIndex + 1, a, b)
                if t <= v: v = t[0], legalActions[i]
                if a >= v: return v
                if b > v: b = v
            return v

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
        "*** YOUR CODE HERE ***"
        _, act = self.expectiMinimax(gameState, 1, 0)
        return act

    def expectiMinimax(self, gameState, depth, agentIndex):
        numAgents = gameState.getNumAgents()
        if depth == self.depth and agentIndex == numAgents - 1:
            return self.evaluationFunction(gameState), ''
        legalActions = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        if len(legalActions) == 0:
            return self.evaluationFunction(gameState), ''
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
        if agentIndex == self.index:
            scores = [self.expectiMinimax(suc, depth, agentIndex + 1)[0] for suc in successorStates]
            result = max(scores)
            return result, legalActions[scores.index(result)]
        elif agentIndex == numAgents - 1:
            scores = [self.expectiMinimax(suc, depth + 1, self.index)[0] for suc in successorStates]
            result = sum(scores) / float(len(legalActions))
            return result, ''
        else:
            scores = [self.expectiMinimax(suc, depth, agentIndex + 1)[0] for suc in successorStates]
            result = sum(scores) / float(len(scores))
            return result, ''

def breadthFirstSearch(startState, isGoalState, i=0):
    # initialize frontier and explored set
    walls = startState.getWalls()
    
    frontier = util.Queue()
    hhhhhhhh = set()
    explored = set()
    length   = dict()

    frontier.push(startState.getPacmanPosition())
    hhhhhhhh.add(startState.getPacmanPosition())
    length[startState.getPacmanPosition()] = 0
    while not frontier.isEmpty():
        chosen = frontier.pop()
        hhhhhhhh.remove(chosen)
        x, y = chosen
        if isGoalState(x, y, i):
            return length[chosen]
        explored.add(chosen)
        successors = []
        for dx, dy in [(1,0), (0,1), (0,-1), (-1,0)]:
            x,y = chosen
            nextx, nexty = int(x + dx), int(y + dy)
            if not walls[nextx][nexty]:
                nextPos = (nextx, nexty)
                successors.append(nextPos)
        for state in successors:
            if state not in hhhhhhhh:
                if state not in explored:
                    frontier.push(state)
                    hhhhhhhh.add(state)
                    length[state] = length[chosen] + 1
    return 0

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currentPos  = currentGameState.getPacmanPosition()

    ghostStates = currentGameState.getGhostStates()
    # scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPos    = []
    scaredPos   = []

    for ghost in ghostStates:
        if ghost.scaredTimer > 1:
            scaredPos.append(ghost.getPosition())
        else:
            ghostPos.append(ghost.getPosition())

    nearestFood  = lambda x, y, _: currentGameState.hasFood(x, y)
    nearestGhost = lambda x, y, _: (x, y) in set(ghostPos)
    nearestScare = lambda x, y, _: (x, y) in set(scaredPos)
    nearestCaps  = lambda x, y, _: (x, y) in currentGameState.getCapsules()
    # findGhost    = lambda x, y, i: (x, y) == ghostPos[i]

    dist2Food  = breadthFirstSearch(currentGameState, nearestFood)
    
    dist2Ghost = 0
    if len(ghostPos) > 0:
        dist2Ghost = breadthFirstSearch(currentGameState, nearestGhost)
    dist2Scared = 0
    if len(scaredPos) > 0:
        dist2Scared = breadthFirstSearch(currentGameState, nearestScare)
    dist2Caps = 10 * len(currentGameState.getCapsules())
    if len(currentGameState.getCapsules()) > 0:
        for x, y in currentGameState.getCapsules():
            if manhattanDistance((x, y), currentPos) < 5:
                continue
            break
        else: dist2Caps = breadthFirstSearch(currentGameState, nearestCaps)

    ghostScoreTotal = 0.791 * dist2Ghost - 5.992 * dist2Scared - 25.07 * len(scaredPos)
    capsScoreTotal  = 19.81 * dist2Caps + 150.43 * len(currentGameState.getCapsules())
    foodScoreTotal  = 0.4947 * dist2Food ** 1.2 + 7.01 * currentGameState.getNumFood()

    result = ghostScoreTotal - 1.2 * capsScoreTotal - 2 * foodScoreTotal + currentGameState.getScore()
    # print result

    return result

    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

