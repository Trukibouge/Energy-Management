import datetime as dt
from dateutil import parser
import numpy as np
from gym.envs.energy.data import DataSet
from gym.envs.energy.time import Clock

class DataBasedForecasteModel(DataSet):
    """
    This class can be useful... it is up to you
    """
    def __init__(self, _capacity, clock):
        super().__init__(_capacity, clock);
        self.dataSet = dataSet;
        self.clock = clock;

    def forecast(self, duration=None, _fromDate=None):
        duration = self.clock.getTimeStepDuration() if duration == None else duration;
        _fromDate = self.clock.getCurrentDateTime()+self.clock.getTimeStepDuration() if _fromDate == None else _fromDate;
        #implement me!!
        return np.zeros(0);

