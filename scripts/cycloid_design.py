import numpy as np
import matplotlib.pyplot as plt 
# from shapely.geometry import Polygon
# from shapely.ops import unary_union
import imageio
from datetime import datetime
import os

class CycloidGeometry:
    def __init__(self):
        self._num_rollers = 10
        self._num_rotors = self._num_rollers - 1
        self._radius_roller_circle = 20
        self._radius_roller = 5
        self._eccentricity = 1 # Must be less than rad_pin_circle / num_rollers
        
        self._radius_output_shaft_pins = 5
        self._radius_output_shaft_circle = 11
        self._num_output_shafts = 5
        
        self._gear_ratio = self.calcGearRatio()
        self._rolling_circle_diam = self.calcRollingCircleDiam()
        self._base_circle_diam = self.calcBaseCircleDiam()
        self._base_hole_diam = self.calcBaseHoleDiameter()
        
        self._rolling_circle_center = []
        self._epicycloid_pts = []
        
        self._valid_roller_value = 3 # Minimum number of rollers
        
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
    def get_base_hole_diam(self) -> float:
        return self._base_hole_diam
    
    @property
    def get_radius_output_shaft_pins(self) -> float:
        return self._radius_output_shaft_pins

    @get_radius_output_shaft_pins.setter
    @check_input((int, float), 1)
    def set_radius_output_shaft_pins(self, radius):
        self._radius_output_shaft_pins = radius
        self._base_hole_diam = self.calcBaseHoleDiameter()

    @property
    def get_radius_output_shaft_circle(self) -> float:
        return self._radius_output_shaft_circle

    @get_radius_output_shaft_circle.setter
    @check_input((int, float), 6)
    def set_radius_output_shaft_circle(self, radius):
        self._radius_output_shaft_circle = radius

    @property
    def get_num_output_shafts(self) -> int:
        return self._num_output_shafts

    @get_num_output_shafts.setter
    @check_input(int, 3)
    def set_num_output_shafts(self, num):
        self._num_output_shafts = num
    
    @property
    def get_last_rolling_circle_center(self) -> list[float]:
        return self._rolling_circle_center[-1::][0]
    
    @property
    def get_last_epicycloid_pts(self) -> list[float]:
        return self._epicycloid_pts[-1::][0]
    
    @property 
    def get_epicycloid_pts(self) -> list[float]:
        return self._epicycloid_pts
    
    @property
    def get_num_rollers(self) -> int:
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
    def get_num_rotors(self) -> int:
        return self._num_rotors
    
    @get_num_rotors.setter
    @check_input(int, 2)
    def set_num_rotors(self, num):
        self._num_rotors = num
        self._num_rollers = num + 1
        self._gear_ratio = self.calcGearRatio()
    
    @property
    def get_radius_roller_circle(self) -> float:
        return self._radius_roller_circle
    
    @get_radius_roller_circle.setter
    @check_input((int, float), 5)
    def set_radius_roller_circle(self, radius):
        self._radius_roller_circle = radius
        self._rolling_circle_diam = self.calcRollingCircleDiam()
        self._base_circle_diam = self.calcBaseCircleDiam()
    
    @property
    def get_radius_roller(self) -> float:
        return self._radius_roller  
    
    @get_radius_roller.setter
    @check_input((int, float), 2)
    def set_radius_roller(self, radius):
        self._radius_roller = radius
    
    @property
    def get_gear_ratio(self):
        return self._gear_ratio
    
    @property
    def get_eccentricity(self) -> float:
        return self._eccentricity
    
    @get_eccentricity.setter
    def set_eccentricity(self, e):
        if (e <= 0 or e > self._radius_roller_circle / self._num_rollers):
            raise ValueError("Eccentricity won't create a valid cycloid.")
        self._eccentricity = e
        
    def calcGearRatio(self):
        return self._num_rotors / (self._num_rollers - self._num_rotors) 
    
    def calcBaseHoleDiameter(self):
        return self._radius_output_shaft_pins + 4 * self._eccentricity # might need to change to 4*e w/ 2 discs
    
    def calcRollingCircleDiam(self):
        return 2 * self._radius_roller_circle / self._num_rollers  
       
    def calcBaseCircleDiam(self):
        return self._gear_ratio * self._rolling_circle_diam
    
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

class CycloidVisualization:
    def __init__(self, cycloid):
        self.cycloid = cycloid
        self.fig = plt.figure(figsize=(4,4))
        self._plot_objects = {}
        
        self.color = 'blue'
        self.alpha = 0.8
        self.frames = []

        self.setupPlot()
    
    def makePlot(self, saveGIF=False, savePic=True):
        self.createPlotShapes()
        self.addPatches()
        self.makeLegendandTitle()
        for angle in range(0, 361):
            self.makeCircleRoll(angle)
            self.updatePatches()
            plt.pause(0.0005)
            self.createPlotGIF()
        if saveGIF: self.saveGIF()
        if savePic: self.savePIC()
            
    def createPlotShapes(self):
        cycloid_base = self.createBaseCircle()
        rolling_circle = self.createRollingCircle()
        rolling_circle_line = self.createRollingCircleLine()
        epicycloid = self.createEpicycloid()
        self._plot_objects = {'cycloid base': cycloid_base, 
                          'rolling circle': rolling_circle,
                          'rolling circle line': rolling_circle_line,
                          'epicycloid': epicycloid}
        self.createCycloidHoles()
    
    def makeCircleRoll(self, angle):
        self.cycloid.calcRollingCircleCenter(angle)
        center = cycloid.get_last_rolling_circle_center
        self.cycloid.createCycloidPts(center, angle)
        
    def updatePatches(self):
        self._plot_objects['rolling circle'].center = \
            self.cycloid.get_last_rolling_circle_center 
        self._plot_objects['rolling circle line'].set_xdata(( \
            self.cycloid.get_last_rolling_circle_center[0],
            self.cycloid.get_last_epicycloid_pts[0]))
        self._plot_objects['rolling circle line'].set_ydata(( \
            self.cycloid.get_last_rolling_circle_center[1],
            self.cycloid.get_last_epicycloid_pts[1]))
        self._plot_objects['epicycloid'].set_xy(self.cycloid.get_epicycloid_pts)
    
    def addPatches(self):
        for key, shape in self._plot_objects.items():
            if key != 'rolling circle line':
                self.ax.add_patch(shape)
            else: 
                self.ax.add_line(shape)
            
    def createBaseCircle(self, center = (0,0)):
        return plt.Circle(center, self.cycloid._base_circle_diam / 2, fill=False, 
                          linestyle='--', label=f'Base Circle, diameter = {self.cycloid._base_circle_diam}') 
    
    def createRollingCircle(self, center = (0,0)):
        return plt.Circle(center, self.cycloid._rolling_circle_diam / 2, fill=False, lw=2,
                          label=f'Rolling Circle, diameter = {self.cycloid._rolling_circle_diam}')
    
    def createRollingCircleLine(self):
        return plt.Line2D((0, 1), (0, 0), color='red', lw=2,
                          label="Rolling Circle Line")
    
    def createEpicycloid(self):
        return plt.Polygon([[0, 0]], fill=False, closed=False, color=self.color,
                           lw=2, alpha = self.alpha,
                           label=f'Epicycloid, eccentricity of {self.cycloid._eccentricity}') 
    
    def createCycloidHoles(self):
        spacing = np.linspace(0, 360, self.cycloid._num_output_shafts + 1)
        for i, output_angle in enumerate(spacing):
            output_hole = plt.Circle(
                (self.cycloid._radius_output_shaft_circle * self.cycloid.cos(output_angle), 
                 self.cycloid._radius_output_shaft_circle * self.cycloid.sin(output_angle)),
                self.cycloid._base_hole_diam / 2, fill=False, color='blue', lw=2)
            self._plot_objects[f'output_hole{i}'] = output_hole
            
    def setupPlot(self):
        axlims = self.calcAxisLimits()
        self.ax = plt.axes(xlim=(-axlims, axlims), ylim=(-axlims, axlims))
        plt.axis('off')
        plt.ion()
        plt.show()
    
    def calcAxisLimits(self):
        return  self.cycloid.get_radius_roller_circle + \
            4 * self.cycloid.get_radius_roller
     
    def makeLegendandTitle(self):
        self.ax.set_title(f"Cycloidal Disc")
        self.fig.legend(framealpha = 0.6, loc='lower center')
    
    def createPlotGIF(self):
        self.fig.canvas.draw()
        frame = np.array(self.fig.canvas.renderer.buffer_rgba())
        self.frames.append(frame)
        
    def saveGIF(self):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H%M")
        imageio.mimsave(f"imgs/plot_ecc_{self.cycloid._eccentricity}_{timestamp}.gif", 
                        self.frames[::4], fps=30)
    
    def savePIC(self):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H%M") 
        filename = f"imgs/cycloid_plot_{timestamp}.png"
        plt.savefig(filename)
    
    def endPlot(self):
        plt.ioff()
        plt.show(block=True)
        
    # TODO: Add holes in cycloid base, add roller pins to plots
    # TODO: Merge Epicycloid and holes into one polygon
    # TODO: Could use LinAlg to implement some equations
    # TODO: Add a secondary plot with cycloidal disc moving around rollers
          
class CycloidSolidWorks:
    def __init__(self, cycloid):
        self.cycloid = cycloid
        self._parameter_list = []
        self._parametric_eqns = []
        self.createTextFile()

    def createTextFile(self):
        os.makedirs('./text', exist_ok=True)
        self.eqn_file_path = os.path.join('./text', 'equations.txt')
        self._eqn_file = open(self.eqn_file_path, "w")
        self._par_eqn_file_path = os.path.join('./text', 'parametric_equations.txt')
        self._par_eqn_file = open(self._par_eqn_file_path, "w")

    def writeParametricEquations(self):
        self.createParametricEqns()
        for line in self._parametric_eqns:
            self._par_eqn_file.write(line)
            self._par_eqn_file.write("\n\n")
        self._par_eqn_file.close()

    def writeParameters(self):
        self.createParameterList()
        for line in self._parameter_list:
            self._eqn_file.write(line)
            self._eqn_file.write("\n\n")
        self._eqn_file.close()

    def createParametricEqns(self):
        ecc = self.cycloid.get_eccentricity
        rollers = self.cycloid.get_num_rollers
        roller_radius = self.cycloid.get_radius_roller
        radius_roller_PCD = self.cycloid.get_radius_roller_circle

        # psi = f"arctan(sin((1-{rollers}) * t) / (((\"D6@Sketch2\" / 2)/({ecc} * {rollers}))-cos((1-{rollers}) * t)))"
        # x = f"x = (\"D6@Sketch2\" / 2) * cos(t) - (\"D7@Sketch2\" / 2) * cos(t + {psi}) - {ecc} * cos({rollers} * t)"
        # y = f"y = -(\"D6@Sketch2\" / 2) * sin(t) + (\"D7@Sketch2\" / 2) * sin(t + {psi}) + {ecc} * sin({rollers} * t)"

        # self._parametric_eqns.append(x)
        # self._parametric_eqns.append(y)

        psi_2 = f"arctan(sin((1-{rollers}) * t) / (({radius_roller_PCD} / ({ecc} * {rollers})) - cos((1 - {rollers}) * t)))"
        x_2 = f"x = {radius_roller_PCD} * cos(t) - {roller_radius} * cos(t + {psi_2}) - {ecc} * cos({rollers} * t)"
        y_2 = f"y = -{radius_roller_PCD} * sin(t) + {roller_radius} * sin(t + {psi_2}) + {ecc} * sin({rollers} * t)"
        
        self._parametric_eqns.append(x_2)
        self._parametric_eqns.append(y_2)

    def createParameterList(self):
        # Append values set in Cycloid Object for Cycloid Disc Creation
        self._parameter_list.append(f"\"roller_radius\"= {self.cycloid.get_radius_roller}mm")
        self._parameter_list.append(f"\"roller_pitch_circle_radius\"= {self.cycloid.get_radius_roller_circle}mm")
        self._parameter_list.append(f"\"num_rollers\"= {self.cycloid.get_num_rollers}")
        self._parameter_list.append(f"\"gear_ratio\"= {self.cycloid.get_gear_ratio}")
        self._parameter_list.append(f"\"eccentricity\"= {self.cycloid.get_eccentricity}")
        self._parameter_list.append(f"\"output_pin_radius\"= {self.cycloid.get_radius_output_shaft_pins}mm")
        self._parameter_list.append(f"\"cycloid_hole_radius\"= {self.cycloid.get_base_hole_diam / 2}mm")
        self._parameter_list.append(f"\"num_output_pins\"= {self.cycloid.get_num_output_shafts}")
        self._parameter_list.append(f"\"base_circle_diameter\"= {self.cycloid.calcBaseCircleDiam()}mm")
        self._parameter_list.append(f"\"output_pin_pitch_radius\"= {self.cycloid.get_radius_output_shaft_circle}mm")
        # Add values for equations in Solidworks

if __name__ == '__main__':
    cycloid = CycloidGeometry()
    cycloid.set_num_rollers = 10
    cycloid.set_radius_roller = 3
    cycloid.set_radius_roller_circle = 20
    cycloid.set_eccentricity = 1.1
    cycloid.set_radius_output_shaft_circle = 10
    cycloid.set_radius_output_shaft_pins = 4
    cycloid.set_num_output_shafts = 4

    # cycloidplot = CycloidVisualization(cycloid)
    # cycloidplot.makePlot(saveGIF=True, savePic=False)   
    # cycloidplot.endPlot()
    cycloid_sldwks = CycloidSolidWorks(cycloid)
    cycloid_sldwks.writeParameters()
    cycloid_sldwks.writeParametricEquations()
    
    
