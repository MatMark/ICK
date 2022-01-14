# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QGroupBox,
                             QHBoxLayout, QLabel, QMenuBar, QPushButton,
                             QVBoxLayout)
import helpers as h


class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("W4N ECG analysis")
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

        menuBar = QMenuBar(self)

        fileMenu = menuBar.addMenu("&File")
        loadAction = QAction("&Load data...", self)
        openAction = QAction("&Open diagnosis...", self)
        saveAction = QAction("&Save diagnosis...", self)
        exitAction = QAction("&Exit", self)

        fileMenu.addAction(loadAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        loadAction.triggered.connect(self.load_data)
        openAction.triggered.connect(self.openDiagnosis)
        saveAction.triggered.connect(self.saveDiagnosis)
        exitAction.triggered.connect(self.close)

        helpMenu = menuBar.addMenu('&Help')
        aboutAction = QAction("&About", self)
        helpAction = QAction("&How to use", self)

        helpMenu.addAction(aboutAction)
        helpMenu.addAction(helpAction)

        aboutAction.triggered.connect(self.showAboutDialog)
        helpAction.triggered.connect(self.showHelpDialog)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        toolbar = NavigationToolbar(self.canvas, self)

        analysisGroupBox = QGroupBox()
        analysislayout = QHBoxLayout()

        pulseGroupBox = QGroupBox()
        diagnosisGroupBox = QGroupBox()
        rhythmGroupBox = QGroupBox()

        pulselayout = QHBoxLayout()
        diagnosislayout = QHBoxLayout()
        rhythmlayout = QHBoxLayout()

        actionsGroupBox = QGroupBox()
        actionslayout = QHBoxLayout()

        # Just some buttons
        buttonLoad = QPushButton('Load data')
        buttonOpenDiagnosis = QPushButton('Open diagnosis')
        buttonSaveDiagnosis = QPushButton('Save diagnosis')
        buttonClose = QPushButton('Exit')

        self.labelPulse = QLabel('Pulse: ---')
        self.pulseHelp = QLabel('?')
        self.pulseHelp.setToolTip('Tooltip for pulse')
        self.labelDiagnosis = QLabel('Diagnosis: ---')
        self.diagnosisHelp = QLabel('?')
        self.diagnosisHelp.setToolTip('Tooltip for diagnosis')
        self.labelRhythm = QLabel('Heart rhythm: ---')
        self.rhythmHelp = QLabel('?')
        self.rhythmHelp.setToolTip('Tooltip for rhythm')

        # adding action to the button
        buttonLoad.clicked.connect(self.load_data)
        buttonLoad.setFixedWidth(200)
        buttonOpenDiagnosis.clicked.connect(self.openDiagnosis)
        buttonOpenDiagnosis.setFixedWidth(200)
        buttonSaveDiagnosis.clicked.connect(self.saveDiagnosis)
        buttonSaveDiagnosis.setFixedWidth(200)
        buttonClose.clicked.connect(self.close)
        buttonClose.setFixedWidth(200)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        pulselayout.addWidget(self.labelPulse)
        pulselayout.addStretch()
        pulselayout.addWidget(self.pulseHelp)
        diagnosislayout.addWidget(self.labelDiagnosis)
        diagnosislayout.addStretch()
        diagnosislayout.addWidget(self.diagnosisHelp)
        rhythmlayout.addWidget(self.labelRhythm)
        rhythmlayout.addStretch()
        rhythmlayout.addWidget(self.rhythmHelp)

        pulseGroupBox.setLayout(pulselayout)
        pulseGroupBox.setFixedHeight(60)
        diagnosisGroupBox.setLayout(diagnosislayout)
        diagnosisGroupBox.setFixedHeight(60)
        rhythmGroupBox.setLayout(rhythmlayout)
        rhythmGroupBox.setFixedHeight(60)

        # adding tool bar to the layout
        actionslayout.addWidget(toolbar)
        # adding push button to the layout
        actionslayout.addWidget(buttonLoad)
        actionslayout.addWidget(buttonOpenDiagnosis)
        actionslayout.addWidget(buttonSaveDiagnosis)
        actionslayout.addWidget(buttonClose)
        actionsGroupBox.setLayout(actionslayout)
        actionsGroupBox.setFixedHeight(60)

        layout.setContentsMargins(10, 30, 10, 10)
        analysislayout.addWidget(pulseGroupBox)
        analysislayout.addWidget(diagnosisGroupBox)
        analysislayout.addWidget(rhythmGroupBox)
        analysisGroupBox.setLayout(analysislayout)
        analysisGroupBox.setFixedHeight(90)
        layout.addWidget(analysisGroupBox)
        # adding canvas to the layout
        layout.addWidget(self.canvas)
        layout.addWidget(actionsGroupBox)

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
        # base line
        base = np.full((self.ecg.size), self.base_y)

        min_var = math.floor(min(self.ecg))
        max_var = math.ceil(max(self.ecg))
        height = int(math.dist([min_var], [max_var]))
        width = height*9/13

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        ax.plot(time, base, color='red', linewidth=1.5)
        ax.plot(time, self.ecg, color='black', linewidth=.5)
        self.show_rr_intervals(ax, rx, ry, min_var)
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

    # show time between R waves
    def show_rr_intervals(self, ax, rx, ry, min_var):
        for i in range(len(rx) - 1):
            point1 = [rx[i], min_var]
            point2 = [rx[i+1], min_var]
            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]
            ax.plot(x_values, y_values, color='c', linestyle="dashed")

            text_x = ((rx[i+1] - rx[i])/2) + rx[i]
            ax.text(text_x - 0.025, min_var + 0.05, "{:.2f}s".format(rx[i+1] - rx[i]), fontsize=10, color="c")

            point1 = [rx[i], min_var]
            point2 = [rx[i], ry[i]]
            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]
            ax.plot(x_values, y_values, color='c', linestyle="dashed")

            point1 = [rx[i+1], min_var]
            point2 = [rx[i+1], ry[i+1]]
            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]
            ax.plot(x_values, y_values, color='c', linestyle="dashed")

    # loading data
    def load_data(self):
        # loading ecg signal from file
        self.ecg, self.fs, self.file_name = h.load_data(self)
        self.analize_signal()

    # signal analizing
    def analize_signal(self):
        if (self.ecg.size > 0):
            # finding R waves
            self.r_x, self.r_y = h.find_r(self.ecg)
            # finding P waves
            self.p_x, self.p_y = h.PWave().find_p(self.ecg, self.r_x)
            # finding base line
            self.base_y = h.find_base(self.ecg)
            # signal length in sec
            self.signal_length = self.ecg.size / self.fs
            # pulse value
            self.pulse = int(60/self.signal_length*len(self.r_x))
            self.labelPulse.setText(f'Pulse: {self.pulse}')
            self.pulseHelp.setToolTip(f'Puls = (60*R)/(n/fs)\n\nGdzie "R" oznacza liczbę wykrytych załamków R\n\
"n" oznacza rzeczywistą liczbę próbek wczytaną z pliku,\n\
a "fs" oznacza częstotliwość próbkowania sygnału w Hz\n\n\
Wykryto {len(self.r_x)} załamków R, wczytano {self.ecg.size} próbek, częstotliwość próbkowania wynosi {self.fs} Hz')
            self.labelDiagnosis.setText(
                f'Diagnosis: {self.checkDiseaseByPulse(self.pulse)}')
            self.labelRhythm.setText(
                f'Heart rhythm: {self.checkRhythm(h.is_regular_rhythm(self.r_x, self.fs))}')
            self.pr_interval = h.PRInterval().get_pr_interval(self.r_x, self.p_x, self.fs)

            self.setWindowTitle(self.file_name)
            self.plot()

    # open diagnosis
    def openDiagnosis(self):
        dialog = h.OpenDiagnosisDialog(parent=self)
        if hasattr(dialog, 'data'):
            diagnosis = dialog.getDiagnosis()
            self.pulse = diagnosis['pulse']
            self.fs = diagnosis['fs']
            self.signal_length = diagnosis['signal_length']
            self.file_name = diagnosis['file_name']
            self.r_x = diagnosis['r_x']
            self.r_y = diagnosis['r_y']
            self.p_x = diagnosis['p_x']
            self.p_y = diagnosis['p_y']
            self.pr_interval = diagnosis['pr_interval']
            self.ecg = np.array(diagnosis['ecg'])
            self.labelPulse.setText(f'Pulse: {self.pulse}')
            self.pulseHelp.setToolTip(diagnosis['pulseHelp'])
            self.labelDiagnosis.setText(f'Diagnosis: {diagnosis["diagnosis"]}')
            self.diagnosisHelp.setToolTip(diagnosis['diagnosisHelp'])
            self.labelRhythm.setText(f'Heart rhythm: {diagnosis["rhythm"]}')
            self.rhythmHelp.setToolTip(diagnosis['rhythmHelp'])

            self.setWindowTitle(self.file_name)
            self.plot()

    # save diagnosis
    def saveDiagnosis(self):
        if hasattr(self, 'pulse'):
            diagDict = {
                "pulse": self.pulse,
                "pulseHelp": self.pulseHelp.toolTip(),
                "diagnosis": self.checkDiseaseByPulse(self.pulse),
                "diagnosisHelp": self.diagnosisHelp.toolTip(),
                "rhythm": self.checkRhythm(h.is_regular_rhythm(self.r_x, self.fs)),
                "rhythmHelp": self.rhythmHelp.toolTip(),
                "pr_interval": self.pr_interval,
                "fs": self.fs,
                "signal_length": self.signal_length,
                "file_name": self.file_name,
                "r_x": self.r_x,
                "r_y": self.r_y,
                "p_x": self.p_x,
                "p_y": self.p_y,
                "ecg": self.ecg.tolist()
            }
            diagnosis = json.dumps(diagDict)
            h.SaveDignosisDialog(parent=self, diagnosis=diagnosis)

    # about dial
    def showAboutDialog(self):
        aboutDialog = h.AboutDialog(parent=self)
        aboutDialog.exec_()

    # help dialog
    def showHelpDialog(self):
        helpDialog = h.HelpDialog(parent=self)
        helpDialog.exec_()

    # bradycardia detection
    def checkBradycardia(self, pulse):
        if(pulse < 60):
            if(pulse > 50):
                self.diagnosisHelp.setToolTip(
                    'Puls jest mniejszy niż 60, ale większy niż 50')
                return str("Probability of Bradycardia")
            else:
                self.diagnosisHelp.setToolTip('Puls jest mniejszy niż 50')
                return str("High probability of Bradycardia")

    # tachycardia detection
    def checkTachycardia(self, pulse):
        if(pulse > 100):
            if(pulse > 120):
                self.diagnosisHelp.setToolTip('Puls jest większy niż 120')
                return str("High probability of Tachycardia")
            else:
                self.diagnosisHelp.setToolTip(
                    'Puls jest większy niż 100, ale mniejszy niż 120')
                return str("Probability of Tachycardia")

    # heart rate based detection disease
    def checkDiseaseByPulse(self, pulse):
        if(self.checkBradycardia(pulse) != None):
            return self.checkBradycardia(pulse)
        elif(self.checkTachycardia(pulse) != None):
            return self.checkTachycardia(pulse)
        else:
            self.diagnosisHelp.setToolTip(
                'Puls jest większy niż 60 i mniejszy niż 100')
            return str("Programmed anomally not found.")

    # checks whether the rhythm is regular or irregular
    def checkRhythm(self, rhythm):
        if rhythm:
            self.rhythmHelp.setToolTip(
                'Rytm serca uznajemy za regularny, gdy odchylenie standardowe różnic pomiędzy załamkami R jest mniejsze niż 0,05 sekund')
            return str("Regular")
        else:
            self.rhythmHelp.setToolTip(
                'Rytm serca uznajemy za nieregularny, gdy odchylenie standardowe różnic pomiędzy załamkami R jest większe lub równe 0,05 sekund')
            return str("Irregular")

    def checkPRInterval(self, interval):
        if 0.12 <= interval <= 0.20:
            return "normal - " + str(round(interval, 3))
        elif interval == -1:
            return "P waves were not detected"
        else:
            return "out of range <0.12, 0.20> - " + str(round(interval, 3))


app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
