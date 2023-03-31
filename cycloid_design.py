import numpy as np
import matplotlib.pyplot as plt 
# import time

class Cycloid:
    def __init__(self):
        # self.num_rotor_teeth = 11
        self._num_rollers = 10
        self._num_rotors = self._num_rollers - 1
        self._radius_pin_circle = 20
        self._radius_roller = 5
        self._eccentricity = 1 # Must be less than rad_pin_circle/ num_rollers
        
        self._gear_ratio = self.calcGearRatio()
        self._rolling_circle_diam = self.getRollingCircleDiam()
        self._base_circle_diam = self.getBaseCircleDiam()
        
        self._rolling_circle_center = []
        self._epicycloid_pts = []
        
        self.color = 'blue'
        self.alpha = 0.8
        
        self._valid_roller_value = 3 # Minimum number of rollers

        #TODO: Add a checker, perhaps a decorator to make sure values are valid
        
    def check_input(valid_types, min_value):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if not isinstance(args[0], valid_types):
                    raise ValueError(f"Input must be of type: {valid_types}")
                if args[0] < min_value:
                    raise ValueError(f"Input must be greater than or equal to {min_value}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def cos(angle):
        return np.cos(np.radians(angle))
    
    @staticmethod
    def sin(angle):
        return np.sin(np.radians(angle))
    
    @property
    def get_last_rolling_circle_center(self):
        return self._rolling_circle_center[-1::][0]
    
    @property
    def get_last_epicycloid_pts(self):
        return self._epicycloid_pts[-1::][0]
    
    @property 
    def get_epicycloid_pts(self):
        return self._epicycloid_pts
    
    @property
    def get_num_rollers(self):
        return self._num_rollers
    
    @get_num_rollers.setter
    @check_input(int, 3)
    def set_num_rollers(self, num):
        self._num_rollers = num
        self._num_rotors = num - 1
        self._gear_ratio = self.calcGearRatio()
        print(f"Number of rollers set to {self._num_rollers}. Number of rotors", 
             f"updated to {self._num_rotors}. Gear ratio is now {self._gear_ratio}")

    @property
    def get_num_rotors(self):
        return self._num_rotors
    
    @get_num_rotors.setter
    @check_input(int, 2)
    def set_num_rotors(self, num):
        self._num_rotors = num
        self._num_rollers = num + 1
        self._gear_ratio = self.calcGearRatio()
    
    @property
    def get_radius_pin_circle(self):
        return self._radius_pin_circle
    
    @get_radius_pin_circle.setter
    @check_input((int, float), 5)
    def set_radius_pin_circle(self, radius):
        self._radius_pin_circle = radius
        self._rolling_circle_diam = self.getRollingCircleDiam()
        self._base_circle_diam = self.getBaseCircleDiam()
        print(f"Radius pin circle: {self._radius_pin_circle}\n",
              f"Rolling circle diameter: {self._rolling_circle_diam}\n",
              f"Base circle diam: {self._base_circle_diam}")
    
    @property
    def get_radius_roller(self):
        return self._radius_roller  
    
    @get_radius_roller.setter
    @check_input((int, float), 2)
    def set_radius_roller(self, radius):
        self._radius_roller = radius
    
    @property
    def get_gear_ratio(self):
        return self._gear_ratio
        
    def calcGearRatio(self):
        return self._num_rotors / (self._num_rollers - self._num_rotors) 
    
    @property
    def get_eccentricity(self):
        return self._eccentricity
    
    @get_eccentricity.setter
    def set_eccentricity(self, e):
        if (e <= 0 or e > self._radius_pin_circle / self._num_rollers):
            raise ValueError("Eccentricity Won't create a valid cycloid.")
        self._eccentricity = e
    
    def getRollingCircleDiam(self):
        return 2 * self._radius_pin_circle / self._num_rollers  
       
    def getBaseCircleDiam(self):
        return self._gear_ratio * self._rolling_circle_diam
    
    def makePlot(self, ax):
        self.createPlotShapes()
        self.addPatches(ax)
        for angle in range(0, 361):
            self.makeCircleRoll(angle)
            self.updatePatches()
            plt.pause(0.001)
            
    def createPlotShapes(self):
        cycloid_base = self.createBaseCircle()
        rolling_circle = self.createRollingCircle()
        rolling_circle_line = self.createRollingCircleLine()
        epicycloid = self.createEpicycloid()
        self._plot_objects = {'cycloid base': cycloid_base, 
                          'rolling circle': rolling_circle,
                          'rolling circle line': rolling_circle_line,
                          'epicycloid': epicycloid}
    
    def makeCircleRoll(self, angle):
        self.calcRollingCircleCenter(angle)
        center = self.get_last_rolling_circle_center
        self.createCycloidPts(center, angle)
        
    def updatePatches(self):
        self._plot_objects['rolling circle'].center = \
            self.get_last_rolling_circle_center 
        self._plot_objects['rolling circle line'].set_xdata(( \
            self.get_last_rolling_circle_center[0],
            self.get_last_epicycloid_pts[0]))
        self._plot_objects['rolling circle line'].set_ydata(( \
            self.get_last_rolling_circle_center[1],
            self.get_last_epicycloid_pts[1]))
        self._plot_objects['epicycloid'].set_xy(self.get_epicycloid_pts)
    
    def addPatches(self, ax):
        for key, shape in self._plot_objects.items():
            if key != 'rolling circle line':
                ax.add_patch(shape)
            else: 
                ax.add_line(shape)
    
    def calcRollingCircleCenter(self, angle):
        x = ((self._base_circle_diam / 2) + (self._rolling_circle_diam / 2)) \
            * self.cos(angle)
        y = ((self._base_circle_diam / 2) + (self._rolling_circle_diam / 2)) \
            * self.sin(angle)
        self._rolling_circle_center.append([x, y])    
    
    def createCycloidPts(self, center: tuple, angle):
        x = center[0] + ((self._rolling_circle_diam / 2) - self._eccentricity) \
            * self.cos(self._num_rollers * angle)
        y = center[1] + ((self._rolling_circle_diam / 2) - self._eccentricity) \
            * self.sin(self._num_rollers * angle)
        self._epicycloid_pts.append([x, y])
            
    def createBaseCircle(self, center = (0,0)):
        return plt.Circle(center, self._base_circle_diam / 2, fill=False, linestyle='--') 
    
    def createRollingCircle(self, center = (0,0)):
        return plt.Circle(center, self._rolling_circle_diam / 2, fill=False, lw=2)
    
    def createRollingCircleLine(self):
        return plt.Line2D((0, 1), (0, 0), color='red', lw=2)
    
    def createEpicycloid(self):
        return plt.Polygon([[0, 0]], fill=False, closed=False, color=self.color,
                           lw=2, alpha = self.alpha)
             

def setupPlot():
    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(xlim=(-30, 30), ylim=(-30, 30)) # TODO: Set axes limits based on size
    plt.axis('off')
    print("setup plot")
    plt.ion()
    plt.show()
    return ax
    
def endPlot():
    print("closing plot")
    plt.ioff()
    plt.show(block=True)

        
if __name__ == '__main__':
    cycloid = Cycloid()
    cycloid.set_num_rollers = 8
    cycloid2 = Cycloid()
    # cycloid.set_radius_pin_circle = 10
    # print(cycloid.get_gear_ratio)
    cycloid.set_eccentricity = 0.9
    
    ax = setupPlot()
    # cycloid2.color = 'magenta'
    # cycloid2.alpha = 0.8
    
    cycloid.makePlot(ax)
    # cycloid2.makePlot(ax)
    
    endPlot()
    
    