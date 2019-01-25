"""
"""
import math
import numpy as np
from gym.envs.energy.energy.energyComponent import EnergyComponent, EnergyComponentModel

class Generator(EnergyComponent):
    """
    Description:
    """
    def __init__(self, memoryCapacity, clock, installedPower, generationModel = None, forecastGenerationModel = None):

        super().__init__(memoryCapacity, clock, generationModel, forecastGenerationModel)
        self.installedPower = installedPower;


class SolarGenerator(Generator):
    """
    Description:
    """
    def __init__(self, memoryCapacity, clock, installedPower, generationModel = None, forecastGenerationModel = None):
        super().__init__(memoryCapacity, clock, installedPower, SolarGeneratorTheoricModel(clock, installedPower) if generationModel == None else generationModel, SolarGeneratorTheoricModel(clock, installedPower) if forecastGenerationModel == None else forecastGenerationModel)        


class SolarGeneratorTheoricModel(EnergyComponentModel):
    def __init__(self, clock, installedPower):
        super().__init__(clock);
        self.installedPower = installedPower;
        self.zenithHour = 12; #Hour at which the sun is in the zenith, this is the spring & autumn value
        self.sunHours = 12; #Number of hours of sun in a day, this is the spring & autumn value
 
    def getEnergyAt(self, step):
        timeStepDurationInHours= self.clock.getTimeStepDurationInHours();
        hour = self.clock.getHourAt(step);
        return self.installedPower * max([0,math.cos(math.pi * (hour - self.zenithHour)/self.sunHours)])*timeStepDurationInHours;


class WindGenerator(Generator):
    """
    Description:
    """
    def __init__(self, memoryCapacity, clock, installedPower, generationModel = None, forecastGenerationModel = None):
        #Implement me!!
        a = 0;
