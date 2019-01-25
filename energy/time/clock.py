
import datetime as dt
from dateutil import parser
class Clock:
    """
    Author: Javier Gil-Quijano (javier.gil-quijano@cea.fr)
    Date : January 2019
    The Clock class implements time mechanisms update for the simulation and the learning tasks.
    The Clock class implements the singleton software pattern, i.e. there is a single instance of  Clock that is shared by the different
    objects and agents of the modelled system.
    The Clock class implements a discrete time evolution mechanism. The Clock class has 3 main attributes:
    -- the timeStepDuration, it is a it datetime.timedelta. It defines the size of the time step, 
    -- the currentTimeStep, it is an integer, it contains the number of time steps since the beginning until the present
    -- the startDateTime, it is datetime. It defines the simulation's start date time, 

    The Clock class implements a discrete time evolution mechanism based on a fixed timeStepDuration
    """    
    class __Clock:

        def __init__(self, timeStepDuration=dt.timedelta(hours=1), startDate = '2018-01-01', startTime = '00:00:00'):
            """
            Parameters : 
            -- timeStepDuration it is a it datetime.timedelta. It defines the size of the time step. By default it is 1 hour
            -- startDate it is a it string, containing the simulation's start date. It must follows the format "aaaa-MM-dd". By default it is '2018-01-01'
            -- startTime it is a it string, containing the simulation's start hour. It must follows the  "hh:mm:ss". By default it is '00:00:00'
            """
            self.currentTimeStep = 0;
            self.timeStepDuration = timeStepDuration;
            self.startDateTime = parser.parse(startDate + ' ' + startTime);
        def __str__(self):
            return repr(self) + self.val
    """
    Single instance of clock
    """
    instance = None

    def __init__(self, timeStepDuration=dt.timedelta(hours=1), startDate = '2018-01-01', startTime = '00:00:00'):
        """
        Constructor
        Parameters : 
        -- timeStepDuration it is a it datetime.timedelta. It defines the size of the time step. By default it is 1 hour
        -- startDate it is a it string, containing the simulation's start date. It must follows the format "aaaa-MM-dd". By default it is '2018-01-01'
        -- startTime it is a it string, containing the simulation's start hour. It must follows the  "hh:mm:ss". By default it is '00:00:00'
        """
        if not Clock.instance:
            Clock.instance = Clock.__Clock(timeStepDuration, startDate, startTime)
        else:
            Clock.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def getStartDateTime(self):
        """
        Returns the startDateTime, it is datetime. It defines the simulation's start date time, 
        """
        return self.instance.startDateTime;

    def getCurrentTimeStep(self):
        """
        Returns the currentTimeStep, it is an integer (>=0), it contains the number of time steps since the beginning until the present
        """
        return self.instance.currentTimeStep;

    def increaseTimeStep(self):
        """
        Increases the currentTimeStep of 1
        """
        self.instance.currentTimeStep += 1;

    def reset(self):
        """
        Sets the currentTimeStep to 0 (go back to the starting point of the simulation)
        """
        self.instance.currentTimeStep = 0;

    def getDateTimeAt(self, timeStep):
        """
        Parameters:
            -- timeStep, an integer >=0
        Returns the datetime corresponding to the given timeStep
        """
        timeStep = max([timeStep, 0]);
        return timeStep*self.getTimeStepDuration() + self.getStartDateTime();

    def getTimeStepAt(self, dateTime):
        """
        Parameters:
            -- dateTime, a datetime
        Returns the timeStep corresponding to the given dateTime, if dateTime <= startDateTime, it returns 0
        """
        dateTime = max([dateTime, self.getStartDateTime()]);
        return int((dateTime - self.getStartDateTime())/self.getTimeStepDuration());

    def getTimeStepDuration(self):
        """
        Returns the timeStepDuration, it is a it datetime.timedelta. It defines the size of the time step, 
        """
        return self.instance.timeStepDuration;

    def durationToSteps(self, duration):
        """
        Parameters:
            -- dateTime, a datetime.timedelta
        Transforms the given duration into time steps number
        """
        return duration / self.getTimeStepDuration();

    def getCurrentDateTime(self):
        """
        Returns the datetime corresponding to the the currentTimeStep, it is the current datetime
        """
        return self.getDateTimeAt(self.getCurrentTimeStep());

    def getTimeStepsPerDay(self):
        """
        Returns the number of time steps of 1 day
        """
        return int(dt.timedelta(hours = 24) / self.getTimeStepDuration());

    def getElapsedTimeStepsForDay(self):
        """
        Returns the number of time steps that have counted for the current day
        """
        return self.getCurrentTimeStep()%self.getTimeStepsPerDay();

    def getHourAt(self, timeStep):
        """
        Returns a real number (0<=h<24) representing the hour of the day. For instance h=0.25, means 00:15:00 
        """
        dateTime = self.getDateTimeAt(timeStep);
        return dateTime.hour + dateTime.minute / 60.0 + dateTime.second / 3600.0;

    def getTimeStepDurationInHours(self):
        """
        Returns the duration of a single time step in hours
        """
        return self.getHourAt(1);

    def getCurrentHour(self):
        """
        Returns a real number (0<=h<24) containing the current hour
        """
        return self.getHourAt(self.getCurrentTimeStep());

