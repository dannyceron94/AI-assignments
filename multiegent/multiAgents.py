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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # found answer in lecure 7 page 30 
        # pac distance to ghost + 1/pac distance to food
        # changed it to 1/pac distance to ghost + 1/pac distance to food because the one above would not give good scores
        
        # tell it that is good when it eats a capsule
        capsuleScore=0
        if(newPos in successorGameState.getCapsules()):
            capsuleScore = 1
        stopScore = 0
        # tell it that is not ok to stand still. force it to look for better paths
        if(action == Directions.STOP):
            stopScore = -1
        scaredScore = 0
        # till is that is it ok to walk around more when the ghost are scared
        if(sum(newScaredTimes)>0):
            scaredScore =1
      
        mininum_ghost_distance = -1
        minumum_food_distance  = -1
    
        #calculating the 
        # calculating the diference distance between the successor ghost and pacman states. we can use the manhattan method from util file

        for ghost in newGhostStates:
            # to get position this goes deep and down to egent state function call.
            # check file pacaman.py file line 154-158 go get the idea of getting the state.
            cghost_distance = manhattanDistance(newPos,ghost.getPosition())
            if(mininum_ghost_distance>= cghost_distance or cghost_distance ==-1):
                mininum_ghost_distance = cghost_distance
            

        # calculating the diference distance between the food  and pacman. we can use the manhattan method from util file.
        # only give it positive if it closer to the food and give it negative if it gers father from the food.
        for food_position in newFood.asList():
            if(successorGameState.hasFood(food_position[0],food_position[1])):
                food_distance = manhattanDistance(newPos,food_position)
                if(minumum_food_distance >= food_distance or minumum_food_distance ==-1):
                    minumum_food_distance = food_distance
        minumum_food_distance = 1/minumum_food_distance
        
    #    suming up all the action's feed back score
        total = mininum_ghost_distance + minumum_food_distance + scaredScore  + stopScore + capsuleScore

        return successorGameState.getScore()+total


        
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #found answer in lecture 7 page 40
        #need pass the gamestate, agentIndex, and depth to keep track how deep we have gone
        # this is a zero-sum problem
        # max is for pacman?
        # n’s*estimate*of*the*children’s*min*is*dropping
        # If*n becomes*worse*than*α,*MAX*will*avoid*it,*so*we*can*
        # prune*n’s*other*children*
        # lagers int value is 2147483647
        def max_value(agentIndex,gameState,depth):
            depth += 1
            # had to add this check else it would not extend more than needed
            # if we reach the botton or a winning state we returns its state value
            if (gameState.isWin() or gameState.isLose() or depth==self.depth):
                return self.evaluationFunction(gameState)
            val = -2147483647
            if(agentIndex==0):
                minAgentIndex = 1
                for action in gameState.getLegalActions(agentIndex):
                    successor= gameState.generateSuccessor(agentIndex,action)
                    val = max(val,value_function(minAgentIndex,successor,depth))
            return val
        
        # picking the min values for the ghosts
        def minimun_value(agentIndex,gameState,depth):
            # if we reach the botton or a winning state we returns its state value
            # this check did does not matter but just to be safe
            if (gameState.isWin() or gameState.isLose() or depth==self.depth): 
                return self.evaluationFunction(gameState)
            val = 2147483647 
            for action in gameState.getLegalActions(agentIndex):
                successor= gameState.generateSuccessor(agentIndex,action)
                # if we reach the max numner of minimixer agent lets max again.
                if agentIndex == (gameState.getNumAgents() - 1):
                    val = min(val,value_function(0,successor,depth))
                else:
                    # keep on calling itself untull there are no more min agents
                    val = min(val,value_function(agentIndex+1,successor,depth))
            return val
        # the main function that checks and calls min and max function depending on type of egent
        def value_function(agentIndex,gameState,depth):
            if (gameState.isWin() or gameState.isLose() or depth==self.depth):
                return self.evaluationFunction(gameState)
                # when engent is 0 we will pick the pacman aka maximaxer
            if(agentIndex==0):
                return max_value(agentIndex,gameState,depth)
                # if the value is greater than 0 we pick the ghost agent aka the minimizer
            else:
                return minimun_value(agentIndex,gameState,depth)

        # starting from the top node
        allValues={}
        minVal = -2147483647
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0,action)
            utility = value_function(1,nextState,0)
            # sotoring all the values into a dictionary to later pick the best value or a specifict action based on the it value if needed
            allValues.update({action:utility})
           
        # returning the best value
        return max(allValues.keys(),key=(lambda k: allValues[k]))

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

        # picking the min values for the ghosts
        def minimun_value(agentIndex,gameState,depth,alpha,beta):
            if (gameState.isWin() or gameState.isLose() or depth==self.depth):
                return self.evaluationFunction(gameState)
            val = 2147483647 
            for action in gameState.getLegalActions(agentIndex):
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    val = min(val,max_value(0,successor,depth,alpha,beta)) 
                else:
                    val = min(val,minimun_value(agentIndex+1,successor,depth,alpha,beta))
                # this is where the pruning of the min take place. 
                if(val<alpha):
                    return val
                beta = min(beta,val)
            return val
       
        def max_value(agentIndex,gameState,depth,alpha,beta):
            depth = depth + 1
            if (gameState.isWin() or gameState.isLose() or depth==self.depth):
                return self.evaluationFunction(gameState)
            val = -2147483647
            if(agentIndex==0):
                minAgentIndex = 1
                for action in gameState.getLegalActions(agentIndex):
                    successor= gameState.generateSuccessor(agentIndex,action)
                    val = max(val,minimun_value(minAgentIndex,successor,depth,alpha,beta))
                     # this is where the pruning of the max take place.  
                    if(val>beta):
                        return val
                    alpha = max(alpha,val)
            return val

        # i really dont need the value_function

        allValues={}
        minVal = -2147483647
        # α:*MAX’s*best*option*on*path*to*root*
        alpha = -2147483647
        # β: MIN’s*best*option*on*path*to*root*
        beta =  2147483647
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0,action)
            utility = minimun_value(1,nextState,0,alpha,beta)
            if(utility>beta):
                return action
            alpha = max(alpha,utility)
            allValues.update({action:utility})
           
        return max(allValues.keys(),key=(lambda k: allValues[k]))
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
        """
        "*** YOUR CODE HERE ***"
        # answer found in lecture 8, page 7
        # only the exp-value function will have the expected value evaluation
        # we will initialize value to  0
        # for this problem will will assime that the probability is distributed equally among the child nodes
        def exp_value(agentIndex,gameState,depth):
            if (gameState.isWin() or gameState.isLose() or depth==self.depth): 
                return self.evaluationFunction(gameState)
            valueSum=0
            numAgents = gameState.getNumAgents()
            for action in gameState.getLegalActions(agentIndex):
                val = 0
                successor= gameState.generateSuccessor(agentIndex,action)
                # in this cases we are not looking for the best min value since this is not an adversarial game type
                if agentIndex == (numAgents - 1):
                    val = value_function(0,successor,depth)
                else:
                    val = value_function(agentIndex+1,successor,depth)
                # we take the same of the values
                valueSum += val
            # we take the probabilty wich is distributed the same among all summed values.
            return valueSum/len(gameState.getLegalActions(agentIndex))

        def max_value(agentIndex,gameState,depth):
            depth +=1 
            if (gameState.isWin() or gameState.isLose() or depth==self.depth):
                return self.evaluationFunction(gameState)
            val = -2147483647
            if(agentIndex==0):
                minAgentIndex = 1
                for action in gameState.getLegalActions(agentIndex):
                    successor= gameState.generateSuccessor(agentIndex,action)
                    val = max(val,value_function(minAgentIndex,successor,depth))
            return val
        
        def value_function(agentIndex,gameState,depth):
            if (gameState.isWin() or gameState.isLose() or depth==self.depth):
                return self.evaluationFunction(gameState)
            if(agentIndex==0):
                return max_value(agentIndex,gameState,depth)
            else:
                return exp_value(agentIndex,gameState,depth)
        
        # collecting all the valuees
        allValues={}
        minVal = -2147483647
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0,action)
            utility = value_function(1,nextState,0)
            allValues.update({action:utility})
        # picking the best value to send back from the dictionary
        return max(allValues.keys(),key=(lambda k: allValues[k]))

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    I tried implementing the evaluation from Q1 but we were not given action. i actually tried to 
    iterate through all the legal actions of the pacman and than calculate the all of its new ghost and food states,
    but I think it was taking too long or the calculation were not right the pacman can timing out. so i just decided
    to use the current states instead but i dont think tbis is right.
    """
    "*** YOUR CODE HERE ***"
    legalActions = currentGameState.getLegalActions()
    final=-2147483647
    finalGameState = currentGameState
    # for action in legalActions:
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
    # currentGameState = ExpectimaxAgent(MultiAgentSearchAgent).getAction(currentGameState)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    scaredScore = 0
    if(sum(newScaredTimes)>0):
        scaredScore =1

    mininum_ghost_distance = -1
    minumum_food_distance  = -1
    currentG = 0
    for ghosts in newGhostStates:
        cghost_distance = manhattanDistance(newPos,ghosts.getPosition())
        if(mininum_ghost_distance>=cghost_distance or cghost_distance == -1):
            mininum_ghost_distance = cghost_distance
        if(1 < mininum_ghost_distance):
            currentG += 1
    for food_position in newFood.asList():
        if(currentGameState.hasFood(food_position[0],food_position[1])):
            food_distance = manhattanDistance(newPos,food_position)
            if(minumum_food_distance >= food_distance or minumum_food_distance ==-1):
                minumum_food_distance = food_distance
        
    minumum_food_distance = 1/minumum_food_distance
    capsuleScore=0
    if(newPos in currentGameState.getCapsules()):
        capsuleScore = 1
    # stopScore = 0
    # if(action == Directions.STOP):
    #     stopScore = -1
    currentPacmanPosition = currentGameState.getPacmanPosition()
    
        # finalGameState = successorGameState
    total = mininum_ghost_distance + minumum_food_distance + scaredScore  + capsuleScore +currentG
    if final<total:
        final = total
    return finalGameState.getScore()+final    

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
