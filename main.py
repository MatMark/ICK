# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                      2021                          |

from matplotlib import ticker
from helpers.load import load_data
from helpers.r import find_r
from helpers.p import PWave

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import math


class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.showFullScreen()
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.setFixedWidth(int(rect.width() * .8))
        self.setFixedHeight(int(rect.height() * .8))
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        self.buttonLoad = QPushButton('Load data')
        # self.buttonPlot = QPushButton('Plot')
        self.buttonClose = QPushButton('Close')

        self.labelPulse = QLabel('Pulse: ---')
        self.labelPulse.setFixedHeight(40)

        self.labelDiagnosis = QLabel('Diagnosis: ---')
        self.labelDiagnosis.setFixedHeight(30)
        # adding action to the button
        self.buttonLoad.clicked.connect(self.load_data)
        # self.buttonPlot.clicked.connect(self.plot)
        self.buttonClose.clicked.connect(self.close)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        layout.addWidget(self.labelPulse)
        layout.addWidget(self.labelDiagnosis)
        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # adding push button to the layout
        layout.addWidget(self.buttonLoad)
        layout.addWidget(self.buttonClose)

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # setting layout to the main window
        self.setLayout(layout)

    # plotting
    def plot(self):
        time = np.arange(self.ecg.size) / self.fs
        # coordinates of R wave
        rx = [x / self.fs for x in self.r_x]
        ry = self.r_y
        # coordinates of P wave
        px = [x / self.fs for x in self.p_x]
        py = self.p_y

        min_var = math.floor(min(self.ecg))
        max_var = math.ceil(max(self.ecg))
        height = int(math.dist([min_var], [max_var]))
        width = height*9/13

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        ax.plot(time, self.ecg, color='black', linewidth=.5)
        ax.plot(rx, ry, color='blue',
                marker='o', linewidth=3, linestyle="None")
        ax.plot(px, py, color='green',
                marker='P', linewidth=3, linestyle="None")

        plt.grid(axis="x", color="r", alpha=.5, linewidth=.5, which='major')
        plt.grid(axis="y", color="r", alpha=.5, linewidth=.5, which='major')
        plt.grid(axis="x", color="r", alpha=.5, linewidth=.2, which='minor')
        plt.grid(axis="y", color='r', alpha=.5, linewidth=.2, which='minor')

        major_locator_x = ticker.MultipleLocator(base=0.2)
        ax.xaxis.set_major_locator(major_locator_x)
        major_locator_y = ticker.MultipleLocator(base=.5)
        ax.yaxis.set_major_locator(major_locator_y)
        minor_locator_x = ticker.AutoMinorLocator(5)
        minor_locator_y = ticker.AutoMinorLocator(5)
        ax.xaxis.set_minor_locator(minor_locator_x)
        ax.yaxis.set_minor_locator(minor_locator_y)

        plt.tick_params(which='major', length=7, color='r')
        plt.tick_params(which='minor', length=4, color='r')
        for spine in ['top', 'right', 'bottom', 'left']:
            ax.spines[spine].set_color('red')
        plt.title(self.file_name + " (przesuw 25mm/s)", fontsize=24)
        plt.xlabel("s", fontsize="20")
        plt.ylabel("mV", fontsize="20")
        plt.xlim(0, width)
        plt.ylim(min_var, max_var)

        self.canvas.draw()

    # loading data
    def load_data(self):
        # loading ecg signal from file
        self.ecg, self.fs, self.file_name = load_data(self)
        # finding R waves
        self.r_x, self.r_y = find_r(self.ecg)
        # finding P waves
        self.p_x, self.p_y = PWave().find_p(self.ecg, self.r_x)
        # signal length in sec
        self.signal_length = self.ecg.size / self.fs
        # pulse value
        self.pulse = int(60/self.signal_length*len(self.r_x))
        self.labelPulse.setText(f'Pulse: {self.pulse}')
        self.labelDiagnosis.setText(
            f'Diagnosis: {self.checkDeseaseByPulse(self.pulse)}')
        self.setWindowTitle(self.file_name)
        self.plot()

    # bradycardia detection
    def checkBradycardia(self, pulse):
        if(pulse < 60):
            if(pulse > 50):
                return str("Probability of Bradycardia")
            else:
                return str("High probability of Bradycardia")

    # tachycardia detection
    def checkTachycardia(self, pulse):
        if(pulse > 100):
            if(pulse > 120):
                return str("High probability of Tachycardia")
            else:
                return str("Probability of Tachycardia")

    # heart rate based detection desease
    def checkDeseaseByPulse(self, pulse):
        if(self.checkBradycardia(pulse) != None):
            return self.checkBradycardia(pulse)
        elif(self.checkTachycardia(pulse) != None):
            return self.checkTachycardia(pulse)
        else:
            return str("Programmed anomally not found.")


app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
