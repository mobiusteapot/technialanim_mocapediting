from enum import Enum
import bezier
import numpy as np

class MovementCurve:
    class Curve_Type(Enum):
        POSITION = 0
        ROTATION = 1
    class Axis(Enum):
        X = 0
        Y = 1
        Z = 2
        W = 3
    class Curve_Shape(Enum):
        DEFAULT = 0

    curve_index = -1
    def __init__(self, curve_type, axis, length, peak, ax = None, curve_shape = Curve_Shape.DEFAULT, frequency = 1):
        MovementCurve.curve_index += 1
        if(curve_type == MovementCurve.Curve_Type.POSITION):
            if(axis == MovementCurve.Axis.W):
                raise Exception("Axis cannot include a w component for a position curve")
        self.curve_type = curve_type
        self.axis = axis
        self.length = length
        self.frequency = frequency
        # switch case for curve shape
        match curve_shape:
            case MovementCurve.Curve_Shape.DEFAULT:
                curve_nodes = np.asfortranarray([[0, peak, self.length], [0, 1,0]])
                #Easier to prefab curve shapes than expose full bezier curves to the constructor
            case _:
                raise Exception("Curve shape not implemented")
        self.ax = ax
        self.curve = bezier.Curve.from_nodes(curve_nodes)
        # Virtually everything below this line is just for plotting
        if(ax is not None):
            self.curve_plot = self.curve.plot(num_pts=self.length, color=self.color_from_axis(), ax=self.ax)
            # Set title to wrap around
            if(self.ax.get_title() != curve_type.name + " " + axis.name + " Curve"):
                title = ax.get_title() 
                if("Position" in title and curve_type == MovementCurve.Curve_Type.ROTATION and "and" not in title):
                    title = title.replace("Position ", "Position and Rotation ")
                elif("Rotation" in title and curve_type == MovementCurve.Curve_Type.POSITION and "and" not in title):
                    title = title.replace("Rotation ", "Position and Rotation ")
                title = title.replace(", ", "")
                title += self.axis.name
                present_axis = []
                if("X" in title):
                    present_axis.append("X")
                if("Y" in title):
                    present_axis.append("Y")
                if("Z" in title):
                    present_axis.append("Z")
                if("W" in title):
                    present_axis.append("W")
                for axis in present_axis:
                    title = title.replace(axis, "")
                title = title.replace(" Curve", ", ".join(present_axis) + " Curve")
                self.ax.set_title(title)
        else:
            self.curve_plot = self.curve.plot(num_pts=self.length)
            self.curve_plot.set_title(str.capitalize(curve_type.name) + " along " + str.capitalize(axis.name) + " Curve")
            self.ax = self.curve_plot.get_figure().axes[0]
        
        self.curve_yvals = self.curve_plot.lines[MovementCurve.curve_index].get_ydata()
        self.curve_plot.get_lines()[MovementCurve.curve_index].set_linestyle(self.line_type_from_curve_type())


    def color_from_axis(self):
        match self.axis:
            case MovementCurve.Axis.X:
                return 'r'
            case MovementCurve.Axis.Y:
                return 'g'
            case MovementCurve.Axis.Z:
                return 'b'
            case MovementCurve.Axis.W:
                return 'y'
    def line_type_from_curve_type(self):
        match self.curve_type:
            case MovementCurve.Curve_Type.POSITION:
                return '--'
            case MovementCurve.Curve_Type.ROTATION:
                return '-'