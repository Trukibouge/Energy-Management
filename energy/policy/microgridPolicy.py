"""
"""

import math
from gym import spaces
import numpy as np
from enum import Enum

class ActionsPolicy(Enum):
    CHARGE_DISCHARGE = 1
    CHARGE_DISCHARGE_IDDLE = 2

class MicrogridPolicy():
    """
    This class provides methods allowing the update of the R.L. policy. You are invited to modify it in order to find the good way to discover/build the policy.
    """
    

    def __init__(self, microgrid):
        
        self.microgrid = microgrid
        """
		Complete this method 
        """
        
    def createActionSpace(self):
        """
		This method initializes the state of actions, it must return a spaces.Discrete space with a given number of values
        In the example we suppose, there are two possible actions
        """
        return spaces.Discrete(3);#Put here the right value

    def createObservationSpace(self):
        """
		This method defines the limits of the observed variables, it is the variables that determine a state it must return a spaces.Box build from the low and high limits for each variable
        The number of constraints (min/max) defined here must be equal to the number of variables in the state and must respect the same order, it is the first constraint corresponds to the first
        variable in the state, and so on
        In the example we consider, that there are N=2 observations variables, the first one varies in the interval [0.3, 10.5], the second one varies in the interval [0.0, 1000]
        """
        
        low = np.array([
            0, #lower limit of the observed variable number 1
            0, #lowerlimit of the observed variable number 2
            0
            ])
        high = np.array([
            10000, #upper limit of the observed variable number 1
            10000, #upper limit of the observed variable number 2
            10000
            ])
        return spaces.Box(low=low, high=high, dtype=np.float32)

    def computeState(self):
        """
		This method defines builds the state at each time step. A state is a numpy.array containing N observation variables
        In the example we consider, that there are 2 observations variables, the constraints on those variables are defined in the createObservationSpace method: In the example :
        -- var1 varies in the interval [0.3, 10.5], 
        -- var2 varies in the interval [0.0, 1000]
        """
        available_energy = self.microgrid.getCurrentStorageGeneration();
        produced_energy = self.microgrid.getCurrentGeneration();
        energy_consumption = self.microgrid.getCurrentConsumption();
        state = (available_energy, produced_energy, energy_consumption);
        return np.array(state);


    def verifyStopConditions(self):
        """
		If this method returns true the current episode is finished 
        This mehtod must then evaluate the conditions where the episode can not continue, for instance, the battery has a negative state of charge 
        """
        
        #In this example we stop when the simulation reaches the 50th time step

        return bool(self.microgrid.clock.getCurrentTimeStep() >=50 or self.computeState()[1] == 0);

    def computeReward(self, done):
        """
		This method computes the reward of a the current state
        The parameter done is the value returned by the verifyStopConditions method
        """
        if not done:
            #still alive
            reward = 10;
        else:
            #bad, something went wrong
            reward = -10;
        return reward


    def improveAction(self, action):
        """
		This method executes the given action. In the createActionSpace we have defined a single action
        The parameter action is the index of the action, given our definition of the actions space, in this example it can be either 0 or 1
        """
        if action == 0:
            #do something
            self.microgrid.storage.iddle(); #asks the storage to do nothing; change for the good action
        else:
            if action == 1:
                #do something else
                self.microgrid.storage.iddle(); #asks the storage to do nothing; change for the good action
            else:
                #It should never happense
                raise('Unknown action ' + str(action));



