from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PyQt5.QtGui import QPalette, QColor
from time import time
from random import randint


INTERVAL = 30 # delay in ms - increase it if the dashboard is freezing, decrease to speed up the update rate

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255)]

class TitleWidget(QtWidgets.QLabel):
    """Widget use to write columns' title"""
    def __init__(self, text, parent=None):
        super(TitleWidget, self).__init__(text, parent)

        # Alignment / Font size
        self.setAlignment(Qt.AlignCenter)
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)

        self.setMinimumSize(160, 0)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        self.setFixedHeight(35)
        

def random_update_plot_data(x, y, mini=0, maxi=200):
    if len(x) == 100:
        x.pop(0) # Remove the first y element.
        x.append(x[-1] + 1)  # Add a new value 1 higher than the last.

        y.pop(0) # Remove the first y element.
        y.append( randint(mini,maxi))  # Add a new random value.
    else:
        x = list(range(100))
        y = [randint(mini, maxi) for _ in range(100)]

    return x, y


class Line(object):
    def __init__(self, graph, num, updateFunction, timer, name=""):
        self.graph = graph
        self.k = num
        self.updateFunction = updateFunction
        self.name = name
        self.x = []
        self.y = []
        pen = pg.mkPen(color=COLORS[self.k])
        self.line = graph.plot(self.x, self.y, name=self.name, pen=pen)

        self.test = 0

        timer.timeout.connect(self.update)

    def update(self):
        if self.test == 0:
            self.x, self.y = self.updateFunction(self.x, self.y)
            self.line.setData(self.x, self.y)
        else:
            self.test = (self.test + 1) % 3


class GraphWidget(pg.PlotWidget):

    def __init__(self, parent, timer, updateFunctions=[random_update_plot_data]*4, dataNames=["test", "ok", "peut-être", None, None]):
        """
            updateFunctions is a list of updateFunction
            updateFunction takes the list of x and y and return the new x and y lists
        """
        super(GraphWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setMinimumWidth(260)

        self.setBackground('w')
        self.setMouseEnabled(x=False, y=False)

        # Labels
        self.setLabel('bottom', 'Time (s)')
        self.addLegend(offset=(1, 1))

        self.nbPlots = len(updateFunctions)
        self.updateFunctions = updateFunctions

        # Init x and y data
        self.x = [[] for _ in range(self.nbPlots)]
        self.y = [[] for _ in range(self.nbPlots)]

        # Init lines
        self.data_lines = [None]*self.nbPlots
        for k in range(self.nbPlots):
            if dataNames is None:
                name = None
            else:
                name = dataNames[k]
            self.data_lines[k] = Line(self, k, self.updateFunctions[k], timer, name=name)


# Temperature
class TempOxidizerGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=-30, maxi=30)
        updateFunctions = [updateFunction]*5
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(-30, 30, padding=0)
        self.setTitle("Oxidizer tank + Passive vent line", color=(0, 0, 0))


class TempPipeworkGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=-30, maxi=30)
        updateFunctions = [updateFunction]*4
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(-30, 30, padding=0)
        self.setTitle("Pipework", color=(0, 0, 0))


class TempInjectorGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=-30, maxi=500)
        updateFunctions = [updateFunction]
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(-30, 500, padding=0)
        self.setTitle("Injector", color=(0, 0, 0))


class TempCombustionGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=0, maxi=200)
        updateFunctions = [updateFunction]*3
        dataNames = ["Wall 1", "Wall 2", "Wall 3"]
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(0, 200, padding=0)
        self.setTitle("Combustion chamber", color=(0, 0, 0))


class TempNozzleGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y)
        updateFunctions = [updateFunction]
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setTitle("Nozzle", color=(0, 0, 0))


# Pression
class PreOxidizerGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=0, maxi=60)
        updateFunctions = [updateFunction]*2
        dataNames = ["Top", "Bottom"]
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(0, 60, padding=0)
        self.setTitle("Oxidizer tank readings", color=(0, 0, 0))


class PreInjectorGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=0, maxi=60)
        updateFunctions = [updateFunction]
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(0, 60, padding=0)
        self.setTitle("Injector", color=(0, 0, 0))


class PreCombustionGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=0, maxi=40)
        updateFunctions = [updateFunction]
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(0, 40, padding=0)
        self.setTitle("Combustion chamber", color=(0, 0, 0))


class PreAmbientGraph(GraphWidget):

    def __init__(self, parent, timer):
        updateFunction = lambda x, y : random_update_plot_data(x, y, mini=0, maxi=2)
        updateFunctions = [updateFunction]*2
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setYRange(0, 1.5, padding=0)
        self.setTitle("Ambient pressure", color=(0, 0, 0))


# Electrical
class HorizontalTextWidget(QtWidgets.QLabel):
    """docstring for TextWidget"""
    def __init__(self, parent, text):
        super(HorizontalTextWidget, self).__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # self.setContentsMargins(left, up, right, down)
        self.setContentsMargins(10, 0, 2, 0)
        self.setFixedHeight(18)


class VerticalTextWidget(QtWidgets.QLabel):
    """docstring for TextWidget"""
    def __init__(self, parent, text):
        super(VerticalTextWidget, self).__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        size = self.minimumSizeHint()
        self.heightOffset = size.width()/2
        self.setMinimumHeight(size.width()+10)
        self.setFixedWidth(size.height()+4)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.translate(0, self.height()/2+self.heightOffset)
        painter.rotate(-90)
        painter.drawText(0, self.width()/2+4, self.text())
        painter.end()


    # def paintEvent(self, event):
    #     QtWidgets.QLabel.paintEvent(self, event)
    #     painter = QtGui.QPainter (self)
    #     painter.translate(0, self.height()-1)
    #     painter.rotate(-90)
    #     self.setGeometry(self.x(), self.y(), self.height(), self.width())
    #     QtWidgets.QLabel.render(self, painter)

    # def minimumSizeHint(self):
    #     size = QtWidgets.QLabel.minimumSizeHint(self)
    #     return QtCore.QSize(size.height(), size.width())

    # def sizeHint(self):
    #     size = QtWidgets.QLabel.sizeHint(self)
    #     return QtCore.QSize(size.height(), size.width())

    # def minimumSizeHint(self):
    #     size = QtWidgets.QLabel.minimumSizeHint(self)
    #     return QtCore.QSize(size.height(), size.width())

    # def sizeHint(self):
    #     size = QtWidgets.QLabel.sizeHint(self)
    #     return QtCore.QSize(size.height(), size.width())


class DataWidget(QtWidgets.QLabel):
    """docstring for DataWidget"""
    def __init__(self, text, timer, updateFunction, fontSize, formatting="{:>5.2f}", parent=None):
        super(DataWidget, self).__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        font = self.font()
        font.setPointSize(fontSize)
        self.setFont(font)

        self.formatting = formatting
        self.updateFunction = updateFunction
        timer.timeout.connect(self.update_value)
    
    def update_value(self):
        value = self.updateFunction()
        if isinstance(value, str):
            self.setText(value)
            return
        self.setText(self.formatting.format(self.updateFunction()))


def random_value(mini=0, maxi=1000):
    return randint(mini,maxi)/100

class Electrical(QtWidgets.QWidget):

    def __init__(self, timer, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        title = TitleWidget("Electrical")

        tab = QtWidgets.QGridLayout()
        tab.setSpacing(2)

        tab.addWidget(VerticalTextWidget(self, "Voltage"), 1, 0)
        tab.addWidget(VerticalTextWidget(self, "Current"), 2, 0)
        tab.addWidget(VerticalTextWidget(self, "Resistance"), 3, 0)

        tab.addWidget(HorizontalTextWidget(self, "Main valve solenoid"), 0, 1)
        tab.addWidget(HorizontalTextWidget(self, "Vent line solenoid"), 0, 2)
        tab.addWidget(HorizontalTextWidget(self, "Ignition system"), 0, 3)

        tab.addWidget(DataWidget("-", timer, random_value, 25), 1, 1)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 1, 2)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 1, 3)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 2, 1)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 2, 2)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 2, 3)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 3, 1)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 3, 2)
        tab.addWidget(DataWidget("-", timer, random_value, 25), 3, 3)

        layout.addWidget(title)
        layout.addLayout(tab)
        self.setLayout(layout)


# Status signals
class ColoredCircle(QtWidgets.QWidget):
    """docstring for ColoredCircle"""
    def __init__(self, timer, parent=None):
        super(ColoredCircle, self).__init__(parent)
        self.status = False
        self.diameter = 30
        self.color = Qt.red

        self.setFixedSize(self.diameter, self.diameter)

        self.variable_for_demo = 0
        timer.timeout.connect(self.update_color)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(QtGui.QBrush(self.color, Qt.SolidPattern))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.diameter, self.diameter)

    def update_color(self):
        self.variable_for_demo = (self.variable_for_demo + 1) % 100
        if self.variable_for_demo == 0:
            self.status = not self.status
            if self.status:
                self.color = Qt.green
            else:
                self.color = Qt.red
            self.update()


class BoolIndicator(QtWidgets.QWidget):
    """docstring for BoolIndicator"""
    def __init__(self, text, timer, parent=None):
        super(BoolIndicator, self).__init__(parent)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(Qt.AlignVCenter)
        # Title
        title = QtWidgets.QLabel(text)
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)

        # Indicator
        indic = ColoredCircle(timer)

        layout.addWidget(title)
        layout.addWidget(indic)

        self.setLayout(layout)
        

class ValueIndicator(QtWidgets.QWidget):
    """docstring for ValueIndicator"""
    def __init__(self, text, timer, updateFunction, sizeTitle=15, sizeData=17, formatting="{}", parent=None):
        super(ValueIndicator, self).__init__(parent)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(Qt.AlignVCenter)
        # Title
        self.title = QtWidgets.QLabel(text)
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = self.title.font()
        font.setPointSize(sizeTitle)
        self.title.setFont(font)

        # Indicator
        self.indic = DataWidget("-", timer, updateFunction, sizeData, formatting=formatting)
        self.indic.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(self.title)
        layout.addWidget(self.indic)

        self.setLayout(layout)


class Status(QtWidgets.QWidget):

    def __init__(self, timer, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        title = TitleWidget("Status signals")
        relief = BoolIndicator("Relief valve trigger", timer)
        valve = BoolIndicator("Abort valve trigger", timer)
        actuation = ValueIndicator("Main valve actuation", timer, lambda: random_value(maxi=10000), formatting="{:.0f} mm")

        layout.addWidget(title)
        layout.addWidget(relief)
        layout.addWidget(valve)
        layout.addWidget(actuation)

        self.setLayout(layout)


# Diagnostic readings
class BoardVoltageIndicator(QtWidgets.QWidget):
    """docstring for BoardVoltageIndicator"""
    def __init__(self, text, timer, parent=None):
        super(BoardVoltageIndicator, self).__init__(parent)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Title
        title = QtWidgets.QLabel(text)
        title.setAlignment(Qt.AlignCenter)
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)

        title.setMaximumHeight(30)

        # Indicators
        indicLayout = QtWidgets.QGridLayout()

        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 0, 0)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 0, 1)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 0, 2)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 0, 3)
        

        layout.addWidget(title)
        layout.addLayout(indicLayout)

        # self.setMinimumWidth(265) # Évite le redimensionnement du widget

        self.setLayout(layout)


class RMCTemperatureIndicator(QtWidgets.QWidget):
    """docstring for RMCTemperatureIndicator"""
    def __init__(self, text, timer, parent=None):
        super(RMCTemperatureIndicator, self).__init__(parent)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        # layout.setAlignment(Qt.AlignVCenter)
        # Title
        title = QtWidgets.QLabel(text)
        title.setAlignment(Qt.AlignCenter)
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)

        title.setMaximumHeight(30)

        # Indicators
        indicLayout = QtWidgets.QGridLayout()

        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 0, 0)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 0, 1)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 1, 0)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 1, 1)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 2, 0)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 2, 1)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 3, 0)
        indicLayout.addWidget(DataWidget("-", timer, random_value, 14), 3, 1)
        

        layout.addWidget(title)
        layout.addLayout(indicLayout)

        self.setLayout(layout)


class ErrorGraph(GraphWidget):

    def __init__(self, timer, parent=None):
        updateFunctions = [random_update_plot_data]
        dataNames = None
        super().__init__(parent, timer, updateFunctions=updateFunctions, dataNames=dataNames)
        self.setTitle("Error", color=(0, 0, 0))
        self.setMaximumHeight(200)


class FPSIndicator(ValueIndicator):
    """docstring for FPSIndicator"""
    def __init__(self, timer, parent=None):
        super(FPSIndicator, self).__init__("FPS :", timer, self.updateFPS,
            sizeTitle=10, sizeData=10,  formatting="{}", parent=parent)
        self.count_frame = 0
        self.interval = 30
        self.time = time()
        self.fps = "-"
        self.setFixedHeight(28)

    def updateFPS(self):
        self.count_frame += 1
        self.count_frame %= self.interval

        if self.count_frame == 0:
            t = time()
            self.fps = int(self.interval / (t - self.time))
            self.time = t
        
        return self.fps 


class Diagnostic(QtWidgets.QWidget):

    def __init__(self, timer, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(570)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        horiLayout = QtWidgets.QHBoxLayout()
        vertLayoutLeft = QtWidgets.QVBoxLayout()
        vertLayoutRight = QtWidgets.QVBoxLayout()

        title = TitleWidget("Diagnostic readings")
        boardVoltage = BoardVoltageIndicator("Board input voltage", timer)
        error = ErrorGraph(timer)
        rmc = RMCTemperatureIndicator("R&MC Temperature", timer)
        fps = FPSIndicator(timer)

        layout.addWidget(title)
        vertLayoutLeft.addWidget(boardVoltage)
        vertLayoutLeft.addWidget(error)
        vertLayoutRight.addWidget(rmc)
        vertLayoutRight.addWidget(fps)
        horiLayout.addLayout(vertLayoutLeft)
        horiLayout.addLayout(vertLayoutRight)
        layout.addLayout(horiLayout)

        
        # print("Board Voltage :", boardVoltage.sizePolicy().horizontalPolicy())
        # # print("Error :", error.sizePolicy().horizontalPolicy())

        # print("Fixed :", QtWidgets.QSizePolicy.Fixed)
        # print("Minimum :", QtWidgets.QSizePolicy.Minimum)
        # print("Maximum :", QtWidgets.QSizePolicy.Maximum)
        # print("Preferred :", QtWidgets.QSizePolicy.Preferred)
        # print("Expanding :", QtWidgets.QSizePolicy.Expanding)
        # print("MinimumExpanding :", QtWidgets.QSizePolicy.MinimumExpanding)
        # print("Ignored :", QtWidgets.QSizePolicy.Ignored)

        # self.aafficher = self
        # timer.timeout.connect(self.print_size)

        self.setLayout(layout)

    # def print_size(self):
    #     print(self.aafficher.frameGeometry().width())


# Main window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.setWindowTitle("Æsir - Engine dashboard")

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(INTERVAL)
        # self.timer.setInterval(1000)

        # Temperature
        # Left Column
        temperatureTitle = TitleWidget("Temperature")
        tempOxidizer = TempOxidizerGraph(self, self.timer)
        tempPipework = TempPipeworkGraph(self, self.timer)
        tempInjector = TempInjectorGraph(self, self.timer)
        tempCombustion = TempCombustionGraph(self, self.timer)
        tempNozzle = TempNozzleGraph(self, self.timer)


        temperature = QtWidgets.QVBoxLayout()
        widgets = [temperatureTitle, tempOxidizer, tempPipework, tempInjector, tempCombustion, tempNozzle]
        
        for w in widgets:
            temperature.addWidget(w)

        # Pressure
        # Middle Column
        pressureTitle = TitleWidget("Pressure")
        preOxidizer = PreOxidizerGraph(self, self.timer)
        preInjector = PreInjectorGraph(self, self.timer)
        preCombustion = PreCombustionGraph(self, self.timer)
        preAmbient = PreAmbientGraph(self, self.timer)

        pressure = QtWidgets.QVBoxLayout()
        widgets = [pressureTitle, preOxidizer, preInjector, preCombustion, preAmbient]
        
        for w in widgets:
            pressure.addWidget(w)

        # Others
        # Right Column
        others = QtWidgets.QVBoxLayout()

        electrical = Electrical(self.timer)
        status = Status(self.timer)
        diagnostic = Diagnostic(self.timer)

        sizePolicy = electrical.sizePolicy()
        sizePolicy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
        electrical.setSizePolicy(sizePolicy)

        # maxWidth = diagnostic.minimumSizeHint().width()
        maxWidth = 500

        electrical.setMaximumWidth(maxWidth)
        status.setMaximumWidth(maxWidth)
        diagnostic.setMaximumWidth(maxWidth)

        others.addWidget(electrical)
        others.addWidget(status)
        others.addWidget(diagnostic)

        # Global layout
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(temperature)
        layout.addLayout(pressure)
        layout.addLayout(others)

        widget = QtWidgets.QWidget(self)
        widget.setLayout(layout)
        
        # Timer for update
        self.timer.start()
        QtCore.QCoreApplication.setQuitLockEnabled(True)
        # Allow the application to end when the window is closed

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)