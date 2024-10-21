import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt


class BloodPressureEntry:
    """Data structure for storing a blood pressure entry."""
    def __init__(self, timestamp, sys, dia, pulse):
        self.timestamp = timestamp
        self.sys = sys
        self.dia = dia
        self.pulse = pulse


class BloodPressureTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blutdruck-Tagebuch")
        self.setGeometry(300, 300, 400, 300)

        # Initialize SQLite database
        self.connection = sqlite3.connect('blood_pressure.db')
        self.create_table()

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input fields for blood pressure data
        self.form_layout = QFormLayout()
        self.sys_input = QLineEdit()
        self.dia_input = QLineEdit()
        self.pulse_input = QLineEdit()

        self.form_layout.addRow("Systolischer Wert (SYS):", self.sys_input)
        self.form_layout.addRow("Diastolischer Wert (DIA):", self.dia_input)
        self.form_layout.addRow("Puls:", self.pulse_input)

        layout.addLayout(self.form_layout)

        # "Eintragen" and "Auswerten" buttons
        self.submit_button = QPushButton("Eintragen")
        self.submit_button.clicked.connect(self.add_entry)
        layout.addWidget(self.submit_button)

        self.evaluate_button = QPushButton("Auswerten")
        self.evaluate_button.clicked.connect(self.show_evaluation_dialog)
        layout.addWidget(self.evaluate_button)

        # Table for displaying entries
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Zeitstempel", "SYS", "DIA", "Puls"])
        layout.addWidget(self.table)

        self.load_entries()  # Load existing entries

    def create_table(self):
        """Creates the table in the SQLite database if it doesn't exist."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blood_pressure (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                sys INTEGER,
                dia INTEGER,
                pulse INTEGER
            )
        ''')
        self.connection.commit()

    def add_entry(self):
        """Adds a new blood pressure entry to the database."""
        try:
            sys_value = int(self.sys_input.text())
            dia_value = int(self.dia_input.text())
            pulse_value = int(self.pulse_input.text())
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add entry to database
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO blood_pressure (timestamp, sys, dia, pulse)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, sys_value, dia_value, pulse_value))
            self.connection.commit()

            # Insert entry into the table view
            entry = BloodPressureEntry(timestamp, sys_value, dia_value, pulse_value)
            self.insert_row(entry)

            # Clear input fields
            self.sys_input.clear()
            self.dia_input.clear()
            self.pulse_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Bitte gültige Werte eingeben!")

    def insert_row(self, entry):
        """Inserts a row into the table view."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(entry.timestamp))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(entry.sys)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(entry.dia)))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(entry.pulse)))

    def load_entries(self):
        """Loads blood pressure entries from the database and displays them in the table."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT timestamp, sys, dia, pulse FROM blood_pressure')
        for timestamp, sys, dia, pulse in cursor.fetchall():
            entry = BloodPressureEntry(timestamp, sys, dia, pulse)
            self.insert_row(entry)

    def show_evaluation_dialog(self):
        """Shows a dialog for evaluation of the blood pressure data."""
        dialog = EvaluationDialog(self.connection, self)
        dialog.exec_()


class EvaluationDialog(QWidget):
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auswertung")
        self.setGeometry(400, 400, 300, 200)

        self.connection = connection
        layout = QVBoxLayout(self)

        self.days_combo = QComboBox()
        self.days_combo.addItems(["Letzte 7 Tage", "Letzte 31 Tage", "Letzte 90 Tage"])
        layout.addWidget(self.days_combo)

        self.show_button = QPushButton("Anzeigen")
        self.show_button.clicked.connect(self.display_data)
        layout.addWidget(self.show_button)

        # Table for displaying evaluation data
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Zeitstempel", "SYS", "DIA", "Puls"])
        layout.addWidget(self.table)

    def display_data(self):
        """Displays blood pressure data in the evaluation table."""
        days = int(self.days_combo.currentText().split()[1])
        threshold_date = datetime.now() - timedelta(days=days)

        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT timestamp, sys, dia, pulse
            FROM blood_pressure
            WHERE timestamp >= ?
        ''', (threshold_date.strftime("%Y-%m-%d %H:%M:%S"),))

        self.table.setRowCount(0)  # Reset the table
        for timestamp, sys, dia, pulse in cursor.fetchall():
            entry = BloodPressureEntry(timestamp, sys, dia, pulse)
            self.insert_row(entry)

    def insert_row(self, entry):
        """Inserts a row into the evaluation table."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(entry.timestamp))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(entry.sys)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(entry.dia)))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(entry.pulse)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BloodPressureTracker()
    window.show()
    sys.exit(app.exec_())
