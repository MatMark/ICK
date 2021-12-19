# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QVBoxLayout


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        helpText = "\
            W górnej części ekranu znajduje się podsumowanie analizy wczytanego sygnału EKG w tym puls, diagnoza i analiza rytmu serca.\n\n\
            W centralnej części ekranu znajduje się miejsce, w którym zostanie wyświetlony wczytany sygnał EKG wraz z zaznaczonymi wykrytymi przez program załamkami R (niebieskie kropki) oraz P (zielone krzyżyki).\n\n\
            W dolnej części ekranu po lewej znajduje się panel sterowania wykresem umożliwiający manipulacje wyświetlanym fragmentem sygnału. Po prawej znajdują się przyciski sterowania programem.\n\n\
* Load data - wczytuje wybrany plik z zapisanym sygnałem EKG\n\
* Open diagnosis - wczytuje zapisaną wcześniej diagnozę\n\
* Save diagnosis - zapisuje przeanalizowany sygnał EKG do pliku wraz z diagnozą\n\
* Exit - kończy działanie programu\n"
        self.setWindowTitle("W4N ECG analysis - help")

        rect = parent.size()
        self.setFixedWidth(int(rect.width() * .4))
        self.setFixedHeight(int(rect.height() * .4))

        about = QLabel(helpText, self)
        about.setFixedWidth(int(rect.width() * .3))
        about.setWordWrap(True)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(about)

        self.setLayout(layout)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        aboutText = "Program zaprojektowany na potrzeby kursu Interakcja Człowiek-Komputer \
na wydziale Informatyki i Telekomunikacji W4N Politechniki Wrocławskiej przez poniższych \
studentów studiów magisterskich na kierunku Informatyka Techniczna:\
\n\n * Miłosz Dziadosz\n * Krystian Kania\n * Mateusz Markowski\n\n\
Prowadzący: dr inż. Jan Nikodem \nRok akademicki: 2021\\2022"
        self.setWindowTitle("W4N ECG analysis - about")

        rect = parent.size()
        self.setFixedWidth(int(rect.width() * .4))
        self.setFixedHeight(int(rect.height() * .4))

        about = QLabel(aboutText, self)
        about.setFixedWidth(int(rect.width() * .3))
        about.setWordWrap(True)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(about)

        self.setLayout(layout)


class OpenDignosisDialog(QDialog):
    def __init__(self, parent=None):
        super(OpenDignosisDialog, self).__init__(parent)
        name = QFileDialog.getOpenFileName(
            self, 'Open File', '', '.diag (*.diag)')[0]
        if name == '':
            return
        file = open(name, 'r')
        self.data = file.read()
        file.close()

    def getDiagnosis(self):
        return json.loads(self.data)


class SaveDignosisDialog(QDialog):
    def __init__(self, parent=None, diagnosis=""):
        super(SaveDignosisDialog, self).__init__(parent)
        name = QFileDialog.getSaveFileName(
            self, 'Save File', '', '.diag (*.diag)')[0]
        if name == '':
            return
        if not name.endswith('.diag'):
            name += '.diag'
        file = open(name, 'w')
        file.write(diagnosis)
        file.close()
