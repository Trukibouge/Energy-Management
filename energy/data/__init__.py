"""
This package contains all the data management classes to simulate the behaviour of a microgrid 
It is defined by 1 hierarchy of classes: 


                        DataSet
                           |
              _____________|___________________________
             |                    |                    |
             |                    |                    |
    PriceDataSet               ExpensesAndIncome      DataBasedForecasteModel*

    * The class DataBasedForecasteModel does not exist, it is a suggestion to create it.
"""
from gym.envs.energy.data.dataSet import DataSet
from gym.envs.energy.data.price import PriceDataSet
from gym.envs.energy.data.price import ExpensesAndIncome
