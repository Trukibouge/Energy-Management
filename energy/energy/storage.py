"""
"""

from gym.envs.energy.energy.energyComponent import EnergyComponent

class Storage(EnergyComponent):
    """
    Author: Javier Gil-Quijano (javier.gil-quijano@cea.fr)
    Date : January 2019
    The Storage class defines the behaviour of a energy storage component. 
    The behaivour of a storage depends on different parameters:
    -- the maxCapabilities of storage, it is the max energy that can be stored
    -- the maxChargePower, it is the max slope of the charging curve
    -- the maxDischargePower, it is the max slope of the discharging curve
    -- the stateOfCharge of the storage, it is a percentage of the energy stored at a given time
    -- the maxStateOfCharge it is the max state of charge accepted for this Storage. By default it is 100%. When the stateOfCharge == maxStateOfCharge, the storage is considered as filled
    -- the minStateOfCharge it is the min state of charge accepted for this Storage. By default it is 0%. When the stateOfCharge == minStateOfCharge, the storage is considered as empty
    3 actions can be performed on the battery :
    -- charge : it is to increase the quantity of energy stored in the battery
    -- discharge : it is to decrease the quantity of energy stored in the battery
    -- iddle : the quantity of energy in the battery does not change
    """
    def __init__(self, maxMemorySize, clock, maxCapabilities, maxChargePower, maxDischargePower, maxStateOfCharge = 100, minStateOfCharge = 0, stateOfCharge = 50):

        super().__init__(maxMemorySize, clock)

        self.maxCapabilities = maxCapabilities;
        self.maxStateOfCharge = maxStateOfCharge;
        self.minStateOfCharge = minStateOfCharge;
        self.stateOfCharge = stateOfCharge;
        self.initStateOfCharge = stateOfCharge;
        self.maxChargePower = maxChargePower;
        self.maxDischargePower = maxDischargePower;


    def update(self, energy):
        """
        Updates the quantity of energy contained in the Storage. Updates the history of energy (see setCurrentEnergy)
        Parameters:
        -- energy a real value, it can be negative, in that case it is considered as a charge energy (it is the stateOfCharge will grow), otherwise is considered as discharge energy (it is the stateOfCharge get lower)
        """
        self.setCurrentEnergy(energy);
        charge = -1*energy;
        self.stateOfCharge = self.stateOfCharge + (self.maxStateOfCharge*charge/self.maxCapabilities);

    def charge(self, speed = 1.0):
        """
        Charge the battery at a given speed (a value between 0 and 1), the charge power used is speed * self.maxChargePower
        Parameters:
        -- speed a real value in [0, 1], if equal to 0, no charge is performed, if between 0 and 1 the charge is performed at the given percentage of the self.maxChargePower
        """
        speed = max([min([1.0, speed]), 0.0]);
        self.update(-1*self.maxChargePower * speed *  self.clock.getTimeStepDurationInHours());

    def discharge(self, speed = 1.0):
        """
        Discharge the battery at a given speed (a value between 0 and 1), the discharge power used is speed * self.maxDishargePower
        Parameters:
        -- speed a real value in [0, 1], if equal to 0, no discharge is performed, if between 0 and 1 the discharge is performed at the given percentage of the self.maxDischargePower
        """
        speed = max([min([1.0, speed]), 0.0]);
        self.update(self.maxDischargePower * speed * self.clock.getTimeStepDurationInHours())

    def iddle(self):
        """
        The battery does nothing in the current step, it is equivalent to call self.discharge or self.charge with speed = 0 
        """
        self.update(0.0)

    def isStateOfChargeCoherent(self):
        """
        Auxiliary function that allows verifying that the state of charge of the Storage is in the interval [self.minStateOfCharge, self.maxStateOfCharge] 
        """
        coherent = (self.stateOfCharge >= self.minStateOfCharge \
                and self.stateOfCharge <= self.maxStateOfCharge)
        return bool(coherent)

    def reset(self):
        """
        sets the state of charge to the self.initStateOfCharge
        """
        super().reset();
        self.stateOfCharge = self.initStateOfCharge;