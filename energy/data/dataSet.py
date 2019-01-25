
import math
import numpy as np
from enum import Enum

class DataSet():
    """
    Author: Javier Gil-Quijano (javier.gil-quijano@cea.fr)
    Date : January 2019
    This class defines a time series with a limited capacity of storage. 
    Data is stored in numpy.array of real data whose size is equal to capacity
    """
    def __init__(self, _capacity, clock):
        """
        Create a data set with the given _capacity and clock
        Parameters:
        -- _capacity an integer > 0
        -- clock a reference to the system clock
        """
        self.clock = clock;
        self.data = np.zeros(max(1,_capacity));
        self.usedSize = 0;

    def capacity(self):
        """
        returns the capacity of storage of this data set. It is an integer greater than 0
        """
        return len(self.data);

    def size(self):
        """
        returns the current used size of this data set. It is an integer lower or equal to self.capacity()
        """
        return self.usedSize;


    def addData(self, data):
        """
        Appends a new data at the end of this data set. If self.size() == self.capacity(), before appending the new data, it shifts all the data between the index 1 and the self.size() to the left.
        It means that the oldest value (at index = 0) is removed.
        """
        if self.size() == self.capacity():
            self.data[0:self.size()-1] = self.data[1:self.size()];
            self.usedSize = self.usedSize -1;
        self.data[self.size()] = data;
        self.usedSize = self.usedSize +1;


    def getLastData(self):
        """
        returns the data at index = size()-1
        """
        return self.data[self.size()-1];

    def getLastNData(self, n):
        """
        returns an numpy.array of real values, containing the data last n appended data, if n  is greater than self.size() it returns an array of self.size() elements (all the data stored in the data set)
        """
        n = min(max([0, n]), self.size());
        return self.data[0:n];

    def getDataForDay(self):
        """
        returns an numpy.array of real values, containing the data stored for the current day, it is the data going from midnight to the current hour
        """
        return self.getLastNData(self.clock.getElapsedTimeStepsForDay())

    def getMax(self):
        """
        returns the max value among all the values stored  in this data set
        """
        return max(self.data);

    def getMin(self):
        """
        returns the min value among all the values stored  in this data set
        """
        return min(self.data);

    def reset(self):
        """
        removes all the stored data 
        """
        for i in range(len(self.data)):
            self.data[i] = 0;
        self.usedSize = 0;

