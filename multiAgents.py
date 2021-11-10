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
        successorGameState = currentGameState.generatePacmanSuccessor(action) #instance
        newPos = successorGameState.getPacmanPosition() #tuple
        newFood = successorGameState.getFood().asList() #instance, a list of t and f
        newGhostStates = successorGameState.getGhostStates() #list
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #list

        "*** YOUR CODE HERE ***"
        eaten = currentGameState.getFood().asList()
        score = successorGameState.getScore() - currentGameState.getScore()
        closestCurr = min([util.manhattanDistance(newPos,state.getPosition())
                           for state in currentGameState.getGhostStates()])
        closestNext = min([util.manhattanDistance(newPos,state.getPosition())
                           for state in newGhostStates])
 
        if action == Directions.STOP:
            score -= 10
            
        if newPos in currentGameState.getCapsules():
            score += 150 * len(successorGameState.getCapsules())
            
        if len(newFood) < len(eaten):
            score += 200
   
        if sum(newScaredTimes) > 0 :
            if closestCurr < closestNext:
                score += 200
            else:
                score -=100
        else:
            if closestCurr < closestNext:
                score -= 100
            else:
                score += 200

        for x in newGhostStates:
            distance = util.manhattanDistance(x.getPosition(),newPos)
            if distance <= 1:
                if (x.scaredTimer != 0):
                    score+=1000
                else:
                    score-=100
        
        return score - 10 * len(newFood)

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
        def MinNode(state1,depth,agentIndex):
            value1 = 999999
            actionlist1 = state1.getLegalActions(agentIndex)
            if state1.isWin() or state1.isLose():
                return self.evaluationFunction(state1)
            for action in actionlist1:
                successor1 = state1.generateSuccessor(agentIndex,action)
                if agentIndex == (state1.getNumAgents() - 1):
                    value1 = min(value1, MaxNode(successor1,depth))
                else:
                    value1 = min(value1,MinNode(successor1,depth,agentIndex+1))
            return value1

        def MaxNode(state2,depth):
            value2 = -999999
            actionlist2 = state2.getLegalActions(0)
            if state2.isWin() or state2.isLose() or (depth + 1)==self.depth:
                return self.evaluationFunction(state2)
            for action in actionlist2:
                successor2 = state2.generateSuccessor(0,action)
                value2 = max(value2,MinNode(successor2,depth + 1,1))
            return value2
        
        actionlist = gameState.getLegalActions(0)
        returnAction = actionlist[0]
        currentScore = MinNode(gameState.generateSuccessor(0,returnAction),0,1)
        for action in actionlist:
            successor = gameState.generateSuccessor(0,action)
            score = MinNode(successor,0,1)
            if score > currentScore:
                returnAction = action
                currentScore = score
        
        return returnAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        "*** YOUR CODE HERE ***"
        """
        
        def MaxNode(state1,depth):
            value1 = -999999
            actionlist1 = state1.getLegalActions(0)
            if state1.isWin() or state1.isLose() or (depth + 1)==self.depth:
                return self.evaluationFunction(state1)
            for action in actionlist1:
                successor1 = state1.generateSuccessor(0,action)
                value1 = max(value1,ExpNode(successor1,depth + 1,1))
            return value1

        def ExpNode(state2, depth, agentIndex):
            value2 = 0.0
            actionlist2 = state2.getLegalActions(agentIndex)
            if state2.isWin() or state2.isLose():
                return self.evaluationFunction(state2)
            if len(actionlist2) == 0:
                return 0
            for action in actionlist2:
                successor2 = state2.generateSuccessor(agentIndex,action)
                if agentIndex == (state2.getNumAgents() - 1):
                    value2 += MaxNode(successor2,depth)
                else:
                    value2 += ExpNode(successor2,depth,agentIndex+1)
            return float(value2)/float(len(actionlist2))
        
        actionlist = gameState.getLegalActions(0)
        returnAction = actionlist[0]
        currentScore = -9999999
        for action in actionlist:
            successor = gameState.generateSuccessor(0,action)
            score = ExpNode(successor,0,1)
            if score > currentScore:
                returnAction = action
                currentScore = score
        
        return returnAction
    
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I created a score depending on the state of the ghosts
                  If the ghosts are scared:
                        Then provide a score that accounts
                        for amt of time scared, distance, and capsules
                  If not then:
                          Calculate score based on distance and capsules
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition() #tuple
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates] #list
    score = currentGameState.getScore()
    
    GhostDistanceTotal = sum([util.manhattanDistance(Pos,state.getPosition())
                       for state in GhostStates])
    CapsulesTotal = len(currentGameState.getCapsules())

    if sum(ScaredTimes) > 0:
        score += sum(ScaredTimes) - (GhostDistanceTotal + CapsulesTotal)
    else:
        score += GhostDistanceTotal + CapsulesTotal

    return score

# Abbreviation
better = betterEvaluationFunction

