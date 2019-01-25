"""
"""

import math
import numpy as np
from gym.envs.energy.energy.storage import Storage
from gym.envs.energy.energy.consumption import Home
from gym.envs.energy.energy.generation import SolarGenerator
from gym.envs.energy.time import Clock;
from gym.envs.energy.data.price import ExpensesAndIncome
from gym.envs.energy.data.dataSet import DataSet

class Microgrid():
    """
    Description:
    """
    
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self, clock, memoryCapacity=24):
        
        """
		Time parameters
        """
        self.memoryCapacity = memoryCapacity;
        self.clock = clock;
        """
		Energy parameters
        """
        self.maxStorageCapabilities = 5.0;
        self.maxChargePower = self.maxStorageCapabilities/10;
        self.maxDischargePower = self.maxStorageCapabilities/10;
        # Zone of utilization of the storage
        self.minStateOfCharge = 0;
        self.maxStateOfCharge = 100;
        self.initStateOfCharge = 50;

        self.storage = None;
        self.generators = [];
        self.consumers = [];
        self.deltaEnergy = DataSet(memoryCapacity, clock);
        self.consumption = DataSet(memoryCapacity, clock);
        self.generation = DataSet(memoryCapacity, clock);
        self.initEnergyComponents();

    def reset(self):
        for i in range(len(self.consumers)):
            self.consumers[i].reset();
        for i in range(len(self.generators)):
            self.generators[i].reset();
        self.storage.reset();
        self.deltaEnergy.reset();
        self.consumption.reset();
        self.generation.reset();


    def initEnergyComponents(self):
        self.initConsumption();
        self.initGeneration();
        self.initStorage();

    def initStorage(self):
        self.storage = Storage(self.memoryCapacity, self.clock, self.maxStorageCapabilities, self.maxChargePower, self.maxDischargePower, 
                self.maxStateOfCharge, self.minStateOfCharge, self.initStateOfCharge);

    def initConsumption(self):
        self.consumers = [];		
        peakPower = 1.0; #max consumed power
        consumer = Home(self.memoryCapacity, self.clock, peakPower)
        self.consumers.append(consumer);		

    def initGeneration(self):
        self.generators = [];		
        installedPower = 1.0; #Max power that can be generated
        solarGenerator = SolarGenerator(self.memoryCapacity, self.clock, installedPower);
        self.generators.append(solarGenerator);

    def getInstalledPower(self):
        installedPower = 0;
        for i in range(len(self.generators)):
            installedPower = installedPower + self.generators[i].installedPower;
        return installedPower;

    def getMaxGeneration(self):
        return self.getInstalledPower() * self.timeStepDurationInHours;

    def getPeakConsumptionPower(self):
        peakPower = 0;
        for i in range(len(self.consumers)):
            peakPower = peakPower + self.consumers[i].peakPower;
        return peakPower;

    def getMaxConsumption(self):
        return self.getPeakConsumptionPower() * self.timeStepDurationInHours;

    def getMaxGeneration(self):
        return self.getInstalledPower() * self.timeStepDurationInHours;

    def getGenerationAt(self, step):
        generation = 0;
        for i in range(len(self.generators)):
            generation = generation + self.generators[i].getEnergyAt(step);
        return generation;

    def getConsumptionAt(self, step):
        consumption = 0;
        for i in range(len(self.consumers)):
            consumption = consumption + self.consumers[i].getEnergyAt(step);
        return consumption;

    def getStorageGenerationAt(self, step):
        return self.storage.getEnergyAt(step);

    def __updateGeneration(self):
        generation = 0;
        for i in range(len(self.generators)):
            self.generators[i].update();
            generation = generation + self.generators[i].getCurrentEnergy();
        self.generation.addData(generation);

    def getCurrentGeneration(self):
        return self.generation.getLastData();

    def __updateConsumption(self):
        consumption = 0;
        for i in range(len(self.consumers)):
            self.consumers[i].update();
            consumption = consumption + self.consumers[i].getCurrentEnergy();
        self.consumption.addData(consumption);

    def getCurrentConsumption(self):
        return self.consumption.getLastData();
        
    def getCurrentStorageGeneration(self):
        return self.storage.getCurrentEnergy();

    def getGenerationForDay(self, step):
        return self.generation.getDataForDay();

    def getStorageGenerationForDay(self, step):
        return self.storage.getEnergyForDay(step);

    def getConsumptionForDay(self, step):
        return self.consumption.getDataForDay();

    def __computeConsumptionGenerationDelta(self):
        return self.getCurrentGeneration() + self.getCurrentStorageGeneration() - self.getCurrentConsumption();
    
    def getCurrentConsumptionGenerationDelta(self):
        return self.deltaEnergy.getLastData();

    def getMaxPositiveImbalance(self):
        return self.getMaxGeneration();

    def getMaxNegativeImbalance(self):
        return self.getMaxConsumption();

    def update(self):
        self.__updateGeneration();
        self.__updateConsumption();
        self.deltaEnergy.addData(self.__computeConsumptionGenerationDelta());


class PriceMicrogrid(Microgrid):
    def __init__(self, clock, priceDataSet, memorySize = 24):
        super().__init__(clock, memorySize);
        self.priceDataSet = priceDataSet;
        self.expensesAndIncome = ExpensesAndIncome(memorySize, clock, priceDataSet);

    def update(self):
        super().update();
        self.priceDataSet.update();
        deltaEnergy = self.getCurrentConsumptionGenerationDelta();
        soldEnergy = deltaEnergy if(deltaEnergy>0) else 0;
        boughtEnergy = -1*deltaEnergy if(deltaEnergy<0) else 0;
        self.expensesAndIncome.setCurrentSoldBoughtEnergy(boughtEnergy, soldEnergy);

    def getCurrentExpensesAndIncomeBalance(self):
        return self.expensesAndIncome.getCurrentBalance();
    
    def getCurrentIncome(self):
        return self.expensesAndIncome.income.getLastData();

    def getCurrentExpenses(self):
        return self.expensesAndIncome.expenses.getLastData();

    def getIncomeForDay(self, step):
        return self.expensesAndIncome.income.getDataForDay();

    def getExpensesForDay(self, step):
        return self.expensesAndIncome.expenses.getDataForDay();

    def getExpensesAndIncomeBalanceForDay(self, step):
        return self.expensesAndIncome.getBalanceForDay(step);

    def getMaxPrice(self):
        return self.priceContainer.getMax();

    def reset(self):
        super().reset;
        self.priceDataSet.reset();
        self.expensesAndIncome.reset();