import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QFileDialog
)
from PyQt5.QtGui import (QColor, QPainter, QPdfWriter, QFont, QTextDocument)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
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
        self.connection = sqlite3.connect('db/blood_pressure.db')
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

            # Clear input fields
            self.sys_input.clear()
            self.dia_input.clear()
            self.pulse_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Bitte gültige Werte eingeben!")

    def load_entries(self):
        """Loads blood pressure entries from the database and displays them in the evaluation table."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT timestamp, sys, dia, pulse FROM blood_pressure')
        for timestamp, sys, dia, pulse in cursor.fetchall():
            entry = BloodPressureEntry(timestamp, sys, dia, pulse)
            self.insert_row(entry)

    def show_evaluation_dialog(self):
        """Shows a dialog for evaluation of the blood pressure data."""
        dialog = EvaluationDialog(self.connection, self)
        dialog.display_data()
        dialog.exec_()

# Enum-like structure for days
class DaysOption:
    LAST_7_DAYS = 7
    LAST_31_DAYS = 31
    LAST_90_DAYS = 90

    @staticmethod
    def get_day_options():
        return {
            "Letzte 7 Tage": DaysOption.LAST_7_DAYS,
            "Letzte 31 Tage": DaysOption.LAST_31_DAYS,
            "Letzte 90 Tage": DaysOption.LAST_90_DAYS
        }

class EvaluationDialog(QDialog):
    # Color attributes for each category
    COLOR_OPTIMAL = QColor(0, 255, 0)  # Green: Optimal
    COLOR_NORMAL = QColor(0, 255, 0)  # Green: Normal
    COLOR_HOCHNORMAL = QColor(255, 255, 0)  # Yellow: Hochnormal
    COLOR_HYPERTONIE_GRAD_1 = QColor(200, 0, 0)  # Red: Hypertonie Grad 1
    COLOR_HYPERTONIE_GRAD_2 = QColor(200, 0, 0)  # Red: Hypertonie Grad 2
    COLOR_HYPERTONIE_GRAD_3 = QColor(200, 0, 0)  # Red: Hypertonie Grad 3
    COLOR_ISOLIERTE_HYPERTONIE = QColor(200, 0, 0)  # Red: Isolierte systolische Hypertonie
    COLOR_DEFAULT = QColor(255, 255, 255)  # White (no category)

        # Class-level variable for the legend HTML
    LEGEND_HTML = """
    <b>Farbcode für Blutdruckkategorien:</b>
    <ul>
        <li><span style="background-color: {COLOR_NORMAL}; padding: 5px;">Grün: Optimal, Normal</span></li>
        <li><span style="background-color: {COLOR_HOCHNORMAL}; padding: 5px;">Gelb: Hochnormal</span></li>
        <li><span style="background-color: {COLOR_HYPERTONIE_GRAD_1}; padding: 5px;">Rot: Hypertonie Grad 1-3, Isolierte systolische Hypertonie</span></li>
    </ul>
    """

    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auswertung")
        self.setGeometry(400, 400, 300, 250)

        self.connection = connection
        layout = QVBoxLayout(self)

                # Legend explaining the color coding
        legend_label = QLabel()
        legend_html = self.LEGEND_HTML.format(
            COLOR_NORMAL=self.COLOR_NORMAL.name(),
            COLOR_HOCHNORMAL=self.COLOR_HOCHNORMAL.name(),
            COLOR_HYPERTONIE_GRAD_1=self.COLOR_HYPERTONIE_GRAD_1.name()
        )

        legend_label.setText(legend_html)  # Set HTML content for legend
        layout.addWidget(legend_label)

        # Create ComboBox with day options
        self.days_combo = QComboBox()
        day_options = DaysOption.get_day_options()

        # Add the options to the ComboBox with human-readable labels
        for label in day_options.keys():
            self.days_combo.addItem(label, day_options[label])
        
        layout.addWidget(self.days_combo)

        # Table for displaying evaluation data
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Zeitstempel", "SYS", "DIA", "Puls"])
        layout.addWidget(self.table)

        # Connect the combo box to automatically update the data on selection change
        self.days_combo.currentIndexChanged.connect(self.display_data)

        # Call display_data initially when the window is shown
        self.display_data()

        # Add PDF export button
        self.pdf_button = QPushButton("Exportieren als PDF")
        self.pdf_button.clicked.connect(self.export_pdf)
        layout.addWidget(self.pdf_button)

    def display_data(self):
        """Displays blood pressure data in the evaluation table."""
        # Get the number of days from the selected combo box item
        days = self.days_combo.currentData()  # Get the associated integer value (7, 31, or 90)
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
        """Inserts a row into the evaluation table with color-coding."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Determine the category and color
        color = self.get_row_color(entry.sys, entry.dia)

        # Insert the values into the table
        self.table.setItem(row_position, 0, QTableWidgetItem(entry.timestamp))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(entry.sys)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(entry.dia)))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(entry.pulse)))

        # Apply color
        self.apply_row_color(row_position, color)

    def apply_row_color(self, row_position, color):
        """Applies the given color to all cells in the specified row."""
        for col in range(4):  # Apply color to all columns in the row
            self.table.item(row_position, col).setBackground(color)

    def get_row_color(self, sys, dia):
        """Determines the color based on the systolic and diastolic values."""
        if sys < 120 and dia < 80:
            return self.COLOR_OPTIMAL  # Green: Optimal
        elif 120 <= sys <= 129 and 80 <= dia <= 84:
            return self.COLOR_NORMAL  # Green: Normal
        elif 130 <= sys <= 139 and 85 <= dia <= 89:
            return self.COLOR_HOCHNORMAL  # Yellow: Hochnormal
        elif 140 <= sys <= 159 and 90 <= dia <= 99:
            return self.COLOR_HYPERTONIE_GRAD_1  # Red: Hypertonie Grad 1
        elif 160 <= sys <= 179 and 100 <= dia <= 109:
            return self.COLOR_HYPERTONIE_GRAD_2  # Red: Hypertonie Grad 2
        elif sys >= 180 and dia >= 110:
            return self.COLOR_HYPERTONIE_GRAD_3  # Red: Hypertonie Grad 3
        elif sys >= 140 and dia < 90:
            return self.COLOR_ISOLIERTE_HYPERTONIE  # Red: Isolierte systolische Hypertonie
        else:
            return self.COLOR_DEFAULT  # Default: White (no category)

    
    ## PDF export functions
    
    def export_pdf(self):
        """Exports the evaluation dialog content to a PDF using HTML rendering."""
        # Create the HTML content for the evaluation
        html_content = self.generate_html_content()

        # Create a QTextDocument to handle the HTML rendering
        document = QTextDocument()
        document.setHtml(html_content)

        # Set up the printer to export to PDF
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("output/evaluation_report.pdf")

        # Print the document to the PDF
        document.print(printer)

        print("PDF exported successfully to evaluation_report.pdf")

    def generate_html_content(self):
        """Generates the HTML content for the evaluation report."""
        
        # Load the CSS from the external file
        with open("res/styles.css", "r") as css_file:
            css_content = css_file.read()

        # HTML content for the legend and table
        html = f"""
        <html>
        <head>
            <style>
            {css_content}
            </style>
        </head>
        <body>
            <div class="legend">
                <b>Farbcode für Blutdruckkategorien:</b>
                <ul>
                    <li><span style="background-color: {self.COLOR_NORMAL.name()}; padding: 5px;">Grün: Optimal, Normal</span></li>
                    <li><span style="background-color: {self.COLOR_HOCHNORMAL.name()}; padding: 5px;">Gelb: Hochnormal</span></li>
                    <li><span style="background-color: {self.COLOR_HYPERTONIE_GRAD_1.name()}; padding: 5px;">Rot: Hypertonie Grad 1-3, Isolierte systolische Hypertonie</span></li>
                </ul>
            </div>
            <table>
                <tr>
                    <th>Zeitstempel</th>
                    <th>SYS</th>
                    <th>DIA</th>
                    <th>Puls</th>
                </tr>
        """
        
        # Fetch the data from the database
        cursor = self.connection.cursor()
        cursor.execute('SELECT timestamp, sys, dia, pulse FROM blood_pressure')  # Ensure query is correct
        rows = cursor.fetchall()

        if not rows:
            print("No data found in the database.")
        
        # Add table rows (replace this with actual data from your database)
        for timestamp, sys, dia, pulse in rows:
            # Get the color for this row based on the blood pressure values
            # Function returns QColor object. only use the .name(), which retrieves hexcode of the color
            color = self.get_row_color(sys, dia).name()  # Get row color based on the blood pressure values
            html += f"""
            <tr style="background-color: {color};">
                <td>{timestamp}</td>
                <td>{sys}</td>
                <td>{dia}</td>
                <td>{pulse}</td>
            </tr>
            """

        # Close the table and return the HTML
        html += "</table></body></html>"
        
        return html


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BloodPressureTracker()
    window.show()
    sys.exit(app.exec_())
