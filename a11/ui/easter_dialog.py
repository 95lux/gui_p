from PyQt5.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QLineEdit, QPushButton, QMessageBox
import datetime
from utils.easter_calculator import calculate_easter, get_holidays

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
