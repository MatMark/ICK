# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |

from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


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
