import math
import numpy as np
import datetime as dt
from gym.envs.energy.data.dataSet import DataSet

class PriceTheoricModel:
    def __init__(self, maxPrice, clock):
        self.maxPrice = maxPrice;
        self.clock = clock;

    def getPriceAt(self, step):
        hour = self.clock.getHourAt(step);
        if hour < 6:
            return 0.6*self.maxPrice;
        elif hour < 9:
            return 0.9*self.maxPrice;
        elif hour < 17:
            return 0.4*self.maxPrice;
        else :
            return self.maxPrice;

    def getCurrentPrice(self):
        return self.getPriceAt(self.clock.getCurrentTimeStep())

class PriceDataSet(DataSet):
    """
    Author: Javier Gil-Quijano (javier.gil-quijano@cea.fr)
    Date : January 2019
    This class extends the DataSet class in order to adapt it to store price data. 
    """
    def __init__(self, memoryCapacity, maxPrice, clock, priceModel = None, forecastPriceModel = None):
        super().__init__(memoryCapacity, clock);
        self.maxPrice = maxPrice;
        self.priceModel = PriceTheoricModel(maxPrice, clock) if priceModel == None else priceModel;
        self.forecastPriceModel = PriceTheoricModel(maxPrice, clock) if forecastPriceModel == None else priceModel;

    def getCurrentPrice(self):
        return self.getLastData();

    def __setCurrentPrice(self, energy):
        self.addData(energy);

    def getPriceForDay(self, step):
        return self.getDataForDay();

    def getMinPrice(self):
        return self.getMin();

    def getMaxPrice(self):
        return self.getMax();

    def update(self):
        self.__setCurrentPrice(self.priceModel.getCurrentPrice());

    def forecastPriceAt(self, step):
        return self.priceModel.getPriceAt(step);


class ExpensesAndIncome(DataSet):
    """
    Description:
    """
    def __init__(self, memoryCapacity, clock, priceContainer):
        super().__init__(memoryCapacity, clock);
        self.priceContainer = priceContainer;
        self.expenses = DataSet(memoryCapacity, clock);
        self.income = DataSet(memoryCapacity, clock);

    def setCurrentSoldBoughtEnergy(self, boughtEnergy = 0.0, soldEnergy=0.0):
        self.income.addData(self.priceContainer.getCurrentPrice()*soldEnergy);
        self.expenses.addData(self.priceContainer.getCurrentPrice()*boughtEnergy);
        self.addData(self.income.getLastData()-self.expenses.getLastData());

    def getBalanceAt(self, step):
        return self.getDataAt(step);

    def getCurrentBalance(self):
        return self.getLastData();

    def getBalanceForDay(self, step):
        return self.getDataForDay();

    def reset(self):
        super().reset();
        self.expenses.reset();
        self.income.reset();