from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database_manager import DatabaseManager
from ui.evaluation_dialog import EvaluationDialog

class BloodPressureTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blutdruck-Tagebuch")
        self.setGeometry(300, 300, 400, 300)
        self.db_manager = DatabaseManager()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.form_layout = QFormLayout()
        self.sys_input = QLineEdit()
        self.dia_input = QLineEdit()
        self.pulse_input = QLineEdit()

        self.form_layout.addRow("Systolischer Wert (SYS):", self.sys_input)
        self.form_layout.addRow("Diastolischer Wert (DIA):", self.dia_input)
        self.form_layout.addRow("Puls:", self.pulse_input)

        layout.addLayout(self.form_layout)

        self.submit_button = QPushButton("Eintragen")
        self.submit_button.clicked.connect(self.add_entry)
        layout.addWidget(self.submit_button)

        self.evaluate_button = QPushButton("Auswerten")
        self.evaluate_button.clicked.connect(self.show_evaluation_dialog)
        layout.addWidget(self.evaluate_button)

    def add_entry(self):
        try:
            sys_value = int(self.sys_input.text())
            dia_value = int(self.dia_input.text())
            pulse_value = int(self.pulse_input.text())
            self.db_manager.add_entry(sys_value, dia_value, pulse_value)
            self.sys_input.clear()
            self.dia_input.clear()
            self.pulse_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Bitte gültige Werte eingeben!")

    def show_evaluation_dialog(self):
        dialog = EvaluationDialog(self.db_manager, self)
        dialog.exec_()