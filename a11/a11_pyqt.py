import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QDialog, QVBoxLayout, QLabel, 
    QRadioButton, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
import datetime


def calculate_easter(year, orthodox=False):
    """Berechnet das Osterdatum für ein gegebenes Jahr."""
    year = int(year)
    if orthodox:
        # Griechisch-Orthodoxe Berechnung (Julianischer Kalender)
        a = year % 19
        b = year % 7
        c = year % 4
        d = (19 * a + 16) % 30
        e = (2 * c + 4 * b + 6 * d) % 7
        day = d + e + 3
        if day > 30:
            easter = datetime.date(year, 5, day - 30)
        else:
            easter = datetime.date(year, 4, day)
    else:
        # Christliche Berechnung (Gregorianischer Kalender)
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        easter = datetime.date(year, month, day)
    return easter


def get_holidays(easter):
    """Gibt Karfreitag, Ostersonntag und Ostermontag zurück."""
    good_friday = easter - datetime.timedelta(days=2)
    easter_monday = easter + datetime.timedelta(days=1)
    return good_friday, easter, easter_monday


class EasterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ostern bestimmen")
        self.setFixedSize(300, 200)

        # Layout
        layout = QVBoxLayout()

        # Radiobuttons
        self.christian_radio = QRadioButton("Christliches Osterfest")
        self.orthodox_radio = QRadioButton("Griechisch-Orthodoxes Osterfest")
        self.christian_radio.setChecked(True)

        # Jahr-Eingabefeld
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Jahr eingeben")

        # "Ostern bestimmen" Button
        self.calc_button = QPushButton("Ostern bestimmen")
        self.calc_button.clicked.connect(self.calculate_easter)

        # "Verlassen" Button
        self.exit_button = QPushButton("Verlassen")
        self.exit_button.clicked.connect(self.close)

        # Layout zusammenbauen
        layout.addWidget(self.christian_radio)
        layout.addWidget(self.orthodox_radio)
        layout.addWidget(self.year_input)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def calculate_easter(self):
        try:
            year = int(self.year_input.text())
            orthodox = self.orthodox_radio.isChecked()
            easter = calculate_easter(year, orthodox)
            good_friday, easter_sunday, easter_monday = get_holidays(easter)

            # Ergebnisfenster anzeigen
            result_message = f"Karfreitag: {good_friday}\nOstersonntag: {easter_sunday}\nOstermontag: {easter_monday}"
            QMessageBox.information(self, "Feiertage", result_message)
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Bitte ein gültiges Jahr eingeben!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Osterfestberechnung")
        self.setGeometry(300, 300, 400, 300)

        # Zentrales Widget und Layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Buttons im Hauptfenster
        self.determine_easter_button = QPushButton("Ostern bestimmen")
        self.determine_easter_button.clicked.connect(self.open_easter_dialog)

        self.exit_button = QPushButton("Beenden")
        self.exit_button.clicked.connect(self.close)

        layout.addWidget(self.determine_easter_button)
        layout.addWidget(self.exit_button)

        self.setCentralWidget(central_widget)

        # Menüleiste
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Datei")
        easter_menu = menubar.addMenu("Ostern bestimmen")

        # Menü-Aktionen
        exit_action = QAction("Beenden", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        determine_easter_action = QAction("Ostern bestimmen", self)
        determine_easter_action.triggered.connect(self.open_easter_dialog)
        easter_menu.addAction(determine_easter_action)

    def open_easter_dialog(self):
        self.dialog = EasterDialog()
        self.dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
