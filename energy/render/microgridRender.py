"""
"""

from gym.envs.energy.render import rendering
import numpy as np


class MicrogridRender():
    """
    Description:
    """
    
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self, microgrid, clock, screen_width = 600, screen_height = 400, horScale = 20, verScale = 50, storageWidth=50, storageHeight=100):
        self.microgrid = microgrid
        self.clock = clock;
        self.viewer = rendering.Viewer(screen_width, screen_height)
        self.screen_width = screen_width;        
        self.screen_height = screen_height;
        self.horScale = horScale;
        self.verScale = verScale;
        self.storageWidth=storageWidth
        self.storageHeight=storageHeight
        self.borderWidth = 0.05*screen_height;
        self.hasPrices = hasattr(microgrid, 'expensesAndIncome'); 
        if not self.hasPrices:
            self.heigthForGraph = (screen_height-2*self.borderWidth)/2;
            self.heigthOrigins = [self.borderWidth, self.borderWidth+ self.heigthForGraph];
        else:
            self.heigthForGraph = (screen_height-2*self.borderWidth)/3;
            self.heigthOrigins = [self.borderWidth, self.borderWidth+ self.heigthForGraph, self.borderWidth+ 2*self.heigthForGraph];

    def renderBox(self, origin, width, height, color = (1.0, 1.0, 1.0)):
        l,r,t,b = origin[0], origin[0]+width, origin[1]+height, origin[1]
        box = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
        box.set_color(color[0], color[1], color[2])
        self.viewer.add_geom(box);


    def renderCurve(self, curve, origin=(0,0), color=(0,0,0), horScale=10, verScale = 10):
        pointsNumber = len(curve)
        points = [];
#        points.append((0,0))
        for i in range(pointsNumber):
            points.append((i*horScale, curve[i]*verScale))
#        points.append(((pointsNumber-1)*horScale, 0))

        curveBox = rendering.PolyLine(points, False);
        curveBox.add_attr(rendering.Transform(translation=origin))
        curveBox.set_color(color[0], color[1], color[2])
        self.viewer.add_geom(curveBox);

    def cleanScreen(self):
        self.renderBox((0,0), self.screen_width, self.screen_height);


    def renderEnergyCurves(self):
        self.cleanScreen();
        self.renderEnergyCurvesWithoutStorage((self.borderWidth +self.storageWidth*1.5, self.heigthOrigins[0]), self.horScale, self.verScale);
        self.renderStorage((self.borderWidth, self.heigthOrigins[1]), self.storageWidth , self.storageHeight )
        self.renderEnergyCurvesWithStorage((self.borderWidth +self.storageWidth*1.5, self.heigthOrigins[1]), self.horScale, self.verScale);
        if self.hasPrices:
            self.renderPrices((self.borderWidth +self.storageWidth*1.5, self.heigthOrigins[2]), self.horScale, self.verScale)

    def renderEnergyCurvesWithoutStorage(self, origin=(0,0), horScale=10, verScale = 10):
        step = self.clock.getCurrentTimeStep();
        generation = self.microgrid.getGenerationForDay(step)
        consumption = self.microgrid.getConsumptionForDay(step)
        zeros = np.zeros(len(generation));
        self.renderCurve(generation, origin, (1, 0, 0), horScale, verScale);
        self.renderCurve(consumption, origin, (0, 0, 1), horScale, verScale);
        self.renderCurve(zeros, origin, (0, 0, 0), horScale, verScale);


    def renderPrices(self, origin=(0,0), horScale=10, verScale = 10):
        step = self.clock.getCurrentTimeStep();
        incomes = self.microgrid.getIncomeForDay(step);
        expenses = self.microgrid.getExpensesForDay(step);

        zeros = np.zeros(len(incomes));
        self.renderCurve(expenses, origin, (1, 0, 0), horScale, verScale);
        self.renderCurve(incomes, origin, (0, 0, 1), horScale, verScale);
        self.renderCurve(zeros, origin, (0, 0, 0), horScale, verScale);

    def renderEnergyCurvesWithStorage(self, origin=(0,0), horScale=10, verScale = 10):
        step = self.clock.getCurrentTimeStep();
        generation = self.microgrid.getGenerationForDay(step)
        consumption = self.microgrid.getConsumptionForDay(step)
        storage = self.microgrid.getStorageGenerationForDay(step)
        generationStorage = np.add(generation, storage);
        zeros = np.zeros(len(generation));
        self.renderCurve(generationStorage, origin, (1, 0, 0), horScale, verScale);
        self.renderCurve(consumption, origin, (0, 0, 1), horScale, verScale);
        self.renderCurve(zeros, origin, (0, 0, 0), horScale, verScale);
        
    def renderStorage(self, origin=(0,0), storageWidth = 50.0, storageHeight = 100.0):
        self.renderBox(origin, storageWidth, storageHeight, (0.0, 0.0, 0.0));
        topWidth = storageWidth/2
        topHeight = topWidth/2
        deltaWidth = storageWidth-topWidth
        self.renderBox((origin[0]+deltaWidth/2, origin[1]+ storageHeight), topWidth, topHeight, (0.0, 0.0, 0.0));
        borderWidth = 0.05*storageWidth;
        maxFilledHeight = storageHeight-2*borderWidth;
        filledHeight = self.microgrid.storage.stateOfCharge*maxFilledHeight/self.microgrid.storage.maxStateOfCharge;
        filledWidth = storageWidth-2*borderWidth;
        self.renderBox((origin[0]+borderWidth, origin[1]+ borderWidth), filledWidth, filledHeight, (0.0, 1.0, 0.0));
        levelsNumber = 10;
        for level in range(1,levelsNumber):
            self.renderBox((origin[0]+borderWidth, origin[1]+ (level*storageHeight/levelsNumber)), filledWidth, borderWidth, (0.0, 0.0, 0.0));


    def render(self, mode='human'):
        self.renderEnergyCurves()
        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
