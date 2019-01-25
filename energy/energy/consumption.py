"""
"""
import math
import numpy as np
from gym.envs.energy.energy.energyComponent import EnergyComponent, EnergyComponentModel

class Consummer(EnergyComponent):
    """
    Description:
    """
    def __init__(self, memoryCapacity, clock, peakPower, consumptionModel = None, forecastConsumptionModel = None):

        super().__init__(memoryCapacity, clock, consumptionModel, forecastConsumptionModel)
        self.peakPower = peakPower;


class Home(Consummer):
    """
    Description:
    """
    def __init__(self, memoryCapacity, clock, peakPower, consumptionModel = None, forecastConsumptionModel = None):
        super().__init__(memoryCapacity, clock, peakPower, HomeConsumptionModel(clock, peakPower) if consumptionModel == None else consumptionModel, HomeConsumptionModel(clock, peakPower) if forecastConsumptionModel == None else consumptionModel )        


class HomeConsumptionModel(EnergyComponentModel):
    def __init__(self, clock, peakPower):
        super().__init__(clock);
        self.peakPower = peakPower;

    def getEnergyAt(self, step):
        timeStepDurationInHours= self.clock.getTimeStepDurationInHours();
        hour = self.clock.getHourAt(step);
        if hour < 6:
            return 0.6*self.peakPower*timeStepDurationInHours;
        elif hour < 9:
            return 0.9*self.peakPower*timeStepDurationInHours;
        elif hour < 17:
            return 0.4*self.peakPower*timeStepDurationInHours;
        else :
            return self.peakPower*timeStepDurationInHours;
 

