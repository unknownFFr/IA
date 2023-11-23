import random

class Q2:
    def __init__(self, alpha : float, gamma : float, eps : float, epsDecay=0.):
        # Agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.epsDecay = epsDecay
        # Possible actions correspond to the set of all x,y coordinate pairs
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        # Initialize Q values to 0 for all state-action pairs.
        # Access value for action a, state s via Q[a][s]
        self.Q = {"1" : {}, "2" : {}}

    def getAction(self, state : str, playerNum : int, p : bool = False):
        """
        Select an action given the current game state.
        """
        possibleActions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
        
        if state not in self.Q:
            self.Q[playerNum][state] = {}
            for action in possibleActions:
                self.Q[state][action] = 0

        # Only consider the allowed actions (empty board spaces)

        if random.random() < self.eps:
            # Random choose.
            action = possibleActions[random.randint(0,len(possibleActions)-1)]
        else:
            # Greedy choose.
            values = [self.Q[playerNum][state][a] for a in possibleActions]
            # Find location of max
            ix_max = [v for v in values if v == max(values)]
            if len(ix_max) > 1:
                # If multiple actions were max, then sample from them
                ix_select = ix_max[random.randint(0, len(ix_max))]
            else:
                # If unique max action, select that one
                ix_select = ix_max[0]

            action = possibleActions[ix_select]
        
        if p:
            print(self.Q[state])
        return action
    
    def update(self, oldState : str, newState : str, action : tuple[int, int], reward : int, playerNum : int):
        """
        Perform the Q-Learning update of Q values.
        """
        # Update Q(s,a)
        if newState is not None:

            if oldState not in self.Q[playerNum]:
                possibleActions = [a for a in self.actions if oldState[a[0]*3 + a[1]] == '-']
                self.Q[playerNum][oldState] = {}
                for action in possibleActions:
                    self.Q[playerNum][oldState][action] = 0

            if newState not in self.Q[playerNum]:
                possibleActions = [a for a in self.actions if newState[a[0]*3 + a[1]] == '-']
                self.Q[playerNum][newState] = {}
                for action in possibleActions:
                    self.Q[playerNum][newState][action] = 0


            possibleActions = [a for a in self.actions if newState[a[0]*3 + a[1]] == '-']
            QValues = [self.Q[playerNum][newState][action] for action in possibleActions]
            
            # update
            sample = reward + self.gamma * max(QValues)
            self.Q[playerNum][oldState][action] = ( 1 - self.alpha ) * self.Q[playerNum][oldState][action] + self.alpha * sample

        else:
            # terminal state update
            self.Q[playerNum][oldState][action] = reward