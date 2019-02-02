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
        return spaces.Discrete(3);

    def createObservationSpace(self):
        """
		This method defines the limits of the observed variables, it is the variables that determine a state it must return a spaces.Box build from the low and high limits for each variable
        The number of constraints (min/max) defined here must be equal to the number of variables in the state and must respect the same order, it is the first constraint corresponds to the first
        variable in the state, and so on
        In the example we consider, that there are N=2 observations variables, the first one varies in the interval [0.3, 10.5], the second one varies in the interval [0.0, 1000]
        """
        
        low = np.array([
            0,
            0,
            0
            ])
        high = np.array([
            10,
            10,
            10
            ])
        return spaces.Box(low=low, high=high, dtype=np.float32)

    def computeState(self):
        """
		This method defines builds the state at each time step. A state is a numpy.array containing N observation variables
        In the example we consider, that there are 2 observations variables, the constraints on those variables are defined in the createObservationSpace method: In the example :
        -- var1 varies in the interval [0.3, 10.5], 
        -- var2 varies in the interval [0.0, 1000]
        """

        generation = self.microgrid.getCurrentGeneration();
        consumption = self.microgrid.getCurrentConsumption();
        #storage = self.microgrid.storage.stateOfCharge;

        storage = self.microgrid.getCurrentStorageGeneration();

        state = (generation, consumption, storage);
        return np.array(state);


    def verifyStopConditions(self):
        """
		If this method returns true the current episode is finished 
        This mehtod must then evaluate the conditions where the episode can not continue, for instance, the battery has a negative state of charge 
        """
        
        #In this example we stop when the simulation reaches the 50th time step
        print("Generation/Consumption/Storage:", self.computeState()[0], " ", self.computeState()[1], " ", self.computeState()[2])
        return bool(self.microgrid.clock.getCurrentTimeStep() >=50 or self.microgrid.storage.isStateOfChargeCoherent() == False);

    def computeReward(self, done):
        """
		This method computes the reward of a the current state
        The parameter done is the value returned by the verifyStopConditions method
        """
        if not done:
            #still alive
            reward = 10;
            
            #Réponse aux besoins en énergie
            if(self.computeState()[1] > self.computeState()[0]):
                if(self.computeState()[2] > 0):
                    reward = reward + 50;
                else:
                    reward = reward - 15;

            else:
                if(self.computeState()[2] < 0):
                    reward = reward + 50;
                else:
                    reward = reward - 15;

           #Objectifs 1 et 2
            if(self.computeState()[2]>0): #Goal 1: increase energy sales
                reward = reward + 10;
            if(self.computeState()[2]<0 and self.computeState()[0]>0.1): #Goal 2: maximization of consumption of local generated energy
                reward = reward + 25;
            elif(self.computeState()[2]<0 and self.computeState()[0]<=0.1): #Goal 2: maximization of consumption of local generated energy
                reward = reward - 100;

        else:
            #bad, something went wrong
            reward = - 200;
        return reward


    def improveAction(self, action):
        """
		This method executes the given action. In the createActionSpace we have defined a single action
        The parameter action is the index of the action, given our definition of the actions space, in this example it can be either 0 or 1
        """
        if action == 0:
            #do something
           self.microgrid.storage.iddle(); #asks the storage to do nothing; change for the good action
        elif action == 1:
                #do something else
                self.microgrid.storage.charge();
        elif action == 2:
                self.microgrid.storage.discharge();
        else:
            #It should never happense
            raise('Unknown action ' + str(action));



