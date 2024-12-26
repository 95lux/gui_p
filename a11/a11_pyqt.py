import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QDialog, QVBoxLayout, QLabel, 
    QRadioButton, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import datetime


def calculate_easter(year, orthodox=False):
    """Berechnet das Osterdatum für ein gegebenes Jahr."""
    
    # Calculation is derived from the well-known easter algorithms
    # Orthodox algorithm derived from https://en.wikipedia.org/wiki/Date_of_Easter
    # Christian algorithm (Gauss easter algorithm) derived from https://www.geeksforgeeks.org/how-to-calculate-the-easter-date-for-a-given-year-using-gauss-algorithm/
    
    year = int(year)
    if orthodox:
        # Griechisch-Orthodoxe Berechnung (Julianischer Kalender)
        # Step 1: Calculate the "Golden Number"
        a = year % 19
        
        # Step 2: Calculate the epact (lunar cycle) for the Julian calendar
        b = year % 7
        c = year % 4
        d = (19 * a + 16) % 30
        e = (2 * c + 4 * b + 6 * d) % 7

        # Step 3: Calculate the date of the Paschal Full Moon
        day = d + e + 3
        if day > 30:
            # Easter falls in May
            easter = datetime.date(year, 5, day - 30)
        else:
            # Easter falls in April
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
        
        self.pixmap = QPixmap('res/easter.jpg')
        self.aspect_ratio = self.pixmap.width() / self.pixmap.height()

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        # Zentrales Widget und Layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

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

        # Move image down
        self.label.move(0, menubar.height())

        # Calculate total required size
        total_height = self.pixmap.height() +  self.menuBar().height()

        # Resize the window to fit the pixmap and additional layout
        self.resize(self.pixmap.width(), total_height)

    def open_easter_dialog(self):
        self.dialog = EasterDialog()
        self.dialog.exec_()

    # overwrites the main windows default resize event, so that aspect ration of the image is preserved 
    def resizeEvent(self, event):
        # Get the new width and enforce the aspect ratio
        new_width = event.size().width()
        new_height = int(new_width / self.aspect_ratio)

        # Restrict the window size to maintain aspect ratio
        self.resize(new_width, new_height)

        # Resize and position the label to fit the new dimensions
        self.label.setGeometry(0, self.menuBar().height(), new_width, new_height)

        # Resize the label to fit the new dimensions
        self.label.setPixmap(self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio))
        
        # Call the parent class resizeEvent
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
