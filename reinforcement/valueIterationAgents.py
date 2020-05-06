# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        #the amount of iteration performed
        for k in range(self.iterations):
            #keeping track of the for each v(s)
            values_s = util.Counter()
            #getting the state
            states = self.mdp.getStates()
            # getting values for each state in states
            for state in states:
                if self.mdp.isTerminal(state):
                    # print("terminsl state reached")
                    values_s.update({state:0})
                else:
                    # calculating the q for each action possible in the curent state
                    actions = self.mdp.getPossibleActions(state)
                    temp = []
                    for action in actions:
                        qv = self.getQValue(state,action)
                        # print("inside for",qv)
                        temp.append(qv)
                        # print("inside for",temp)
                        
                    qMAXs = max(temp)
                    values_s.update({state:qMAXs})
            self.values = values_s




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # same as maxV(s)
    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitions  = self.mdp.getTransitionStatesAndProbs(state,action)
        qValSum=0
        # sum happening here
        for transition in transitions:
            nextState   = transition[0]
            probability = transition[1]
            reward  = self.mdp.getReward(state,action,nextState)
            # sum happening here
            qValSum += probability*(reward+ self.discount*(self.values[nextState]))
        # print("the q vale is ",qValSum)
        return qValSum    
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestPolicy = util.Counter()
        for action in self.mdp.getPossibleActions(state):
            bestPolicy[action] = self.getQValue(state, action)

        return bestPolicy.argMax()
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
          #the amount of iteration performed
        # print("\n")
        for k in range(self.iterations):
            #keeping track of the for each v(s)
            values_s = util.Counter()
            #getting the state
            states = self.mdp.getStates()
            # getting values for each state in states
            # tempk = k
            # if(k == len(states)-1):
            #     k = 0
            indexState = k%len(states)
            # print(indexState)
            state = states[indexState]
            # k = tempk
            if self.mdp.isTerminal(state):
                # print("terminsl state reached")
                continue
            else:
                    # calculating the q for each action possible in the curent state
                actions = self.mdp.getPossibleActions(state)
                temp = []
                for action in actions:
                    qv = self.getQValue(state,action)
                        # print("inside for",qv)
                    temp.append(qv)
                        # print("inside for",temp)
                        
                qMAXs = max(temp)
                    # values_s.update({state:qMAXs})
                self.values[state] = qMAXs

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #1 compute predecessors of all states
        states = self.mdp.getStates()
        # 2 Initialize an empty priority queue
        priQ = util.PriorityQueue()
        # 3 for each non terminal state
        states = self.mdp.getStates()
        for state in states:
            if(self.mdp.isTerminal(state)):
                continue
            else:
                # calculating abs of the diff btw current val and the maxq
                actions = self.mdp.getPossibleActions(state)
                temp = []
                for action in actions:
                    qv = self.getQValue(state,action)
                        # print("inside for",qv)
                    temp.append(qv)
                        # print("inside for",temp)
                        
                qMAXs = max(temp)
                diff = abs(self.values[state]-qMAXs)
                # push s into priority with -diff
                priQ.update(state,-diff)
        # stores all the predecessor of s because when i tried to do it later it did not work
        predecessor = {}
        for state in states:
            if self.mdp.isTerminal(state):
                continue
            for act in self.mdp.getPossibleActions(state):
                for transac in self.mdp.getTransitionStatesAndProbs(state, act):
                    next_state = transac[0]
                    if next_state in predecessor:
                        predecessor[next_state].add(state)
                    else:
                        predecessor[next_state] = {state}
        # 4 for iteration in 0...
        for k in range(self.iterations):
            if priQ.isEmpty():
                break
            s = priQ.pop()
            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                temp = []
                for action in actions:
                    qv = self.getQValue(s,action)
                        # print("inside for",qv)
                    temp.append(qv)
                        # print("inside for",temp)
                self.values[s] =max(temp)
                
            # could maybe be implemented differently
            for pred in predecessor[s]:
                if (self.mdp.isTerminal(pred)):
                    continue
                actions = self.mdp.getPossibleActions(pred)
                tempSum = []
                for action in actions:
                    qval = self.getQValue(pred,action)
                        # print("inside for",qv)
                    tempSum.append(qval)
                diff = abs(self.values[pred]-max(tempSum))
                if(diff > self.theta):
                    priQ.update(pred, -diff)
                
            # for act in self.mdp.getPossibleActions(s):
            #     for tran in self.mdp.getTransitionStatesAndProbs(s, act):
            #         tempT =[]
            #         if(self.mdp.isTerminal(tran[0])):
            #             continue
            #         for actt in self.mdp.getPossibleActions(tran[0]):
            #             qv = self.getQValue(tran[0],actt)
            #             tempT.append(qv)
            #         differ = abs(self.values[tran[0]]-max(tempT))
            #         if(differ > self.theta):
            #             priQ.update(tran[0],-differ)