"""
"""

import math
import datetime as dt
import gym
from gym import spaces, logger
from gym.utils import seeding
from gym.envs.classic_control import rendering
import numpy as np
from enum import Enum
from gym.envs.energy.render import MicrogridRender
from gym.envs.energy.energy import Microgrid, PriceMicrogrid
from gym.envs.energy.data import PriceDataSet
from gym.envs.energy.policy import MicrogridPolicy
from gym.envs.energy.time import Clock;

class MicrogridMode(Enum):
    """
    This enum can be useful. It is up to you
    """
    CONNECTED = 1
    ISLANDED = 2

class MicrogridEnv(gym.Env):
    """
    Author: Javier Gil-Quijano (javier.gil-quijano@cea.fr)
    Date : January 2019
   This class defines the reinforcement learning environment you can modify the __init__ method if you consider necessary. I advice you to do not change the other methods.
    You are invited also to modify the MicrogridPolicy (gym.envs.energy.policy.microgridPolicy.py)
    """
    
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        

        """
		Time parameters
        """
        timeStepDurationInHours = 1; #1 hour
        self.memorySizePerDay = int(24/timeStepDurationInHours); #number of time steps per day
        self.clock = Clock(dt.timedelta(hours=timeStepDurationInHours));
        memorySize = 72;
        """
		Energy parameters
        """
        self.microgrid = Microgrid(self.clock, memorySize);
        """
		Learning parameters
        """
        self.seed()
        self.state = None
        self.steps_beyond_done = None
        self.microgridPolicy = MicrogridPolicy(self.microgrid)
        self.initObservationAndActionSpaces();


        """
		Visualization parameters
        """
        self.microgridRender = None; 
        self.viewer = None

    def initObservationAndActionSpaces(self):
        """
		Calls the self.microgridPolicy and initializes the action and observation (state) spaces
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        self.action_space = self.microgridPolicy.createActionSpace();
        self.observation_space = self.microgridPolicy.createObservationSpace();

    def updateState(self):
        """
		Asks the self.microgridPolicy to compute the current state 
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        self.state = self.microgridPolicy.computeState();

    def seed(self, seed=None):
        """
		Initializes the random generators seed
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        """
		This method is called at the end of each episode, it reset all the elements in order to be able to restart a new episode
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        self.clock.reset()
        self.microgrid.reset();
        self.steps_beyond_done = None
        self.updateState();
        return self.state

    def step(self, action):
        """
		This method is called at each time step. It computes the next action, state and reward
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        self.microgridPolicy.improveAction(action);

        self.microgrid.update();

        self.updateState();
        done =  self.microgridPolicy.verifyStopConditions();
        reward = self.microgridPolicy.computeReward(done)
        if done: 
            if self.steps_beyond_done is None:
                self.steps_beyond_done = 0
            else:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
                self.steps_beyond_done += 1
        self.clock.increaseTimeStep();
        return self.state, reward, done, {}


    def render(self, mode='human'):
        """
		Asks the GUI to update its state
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        if self.microgridRender == None : self.microgridRender = MicrogridRender(self.microgrid, self.clock);	
        self.microgridRender.render(mode);

    def close(self):
        """
		If the GUI is closed
        !!!!DO NOT CHANGE THIS FUNCTION
        """
        self.microgridRender.close();
