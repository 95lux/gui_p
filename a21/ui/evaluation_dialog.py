from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QColor, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from datetime import datetime, timedelta
from blood_pressure_entry import BloodPressureEntry
from days_option import DaysOption

class EvaluationDialog(QDialog):
    COLOR_OPTIMAL = QColor(0, 255, 0)               # Optimal: Green
    COLOR_NORMAL = QColor(0, 200, 0)                # Normal: A slightly darker Green

    COLOR_HOCHNORMAL = QColor(255, 255, 0)          # Light Yellow

    COLOR_HYPERTONIE_GRAD_1 = QColor(255, 100, 100) # Light Red for Grad 1
    COLOR_HYPERTONIE_GRAD_2 = QColor(255, 50, 50)   # Darker Red for Grad 2
    COLOR_HYPERTONIE_GRAD_3 = QColor(200, 0, 0)     # Dark Red for Grad 3
    COLOR_ISOLIERTE_HYPERTONIE = QColor(200, 0, 0)  # Same as Hypertonie Grad 3
    
    COLOR_DEFAULT = QColor(255, 255, 255)           # White (no category)

    # HTML Legend with Table for Blood Pressure Categories and Values
    LEGEND_HTML = f"""
    <b>Farbcode für Blutdruckkategorien:</b>
    <table border="1" cellpadding="3" cellspacing="0">
        <thead>
            <tr>
                <th>Blutdruckkategorie</th>
                <th>Systolischer Wert</th>
                <th>Diastolischer Wert</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="background-color: {COLOR_OPTIMAL.name()};">Optimal</td>
                <td>unter 120</td>
                <td>unter 80</td>
            </tr>
            <tr>
                <td style="background-color: {COLOR_NORMAL.name()};">Normal</td>
                <td>120 bis 129</td>
                <td>80 bis 84</td>
            </tr>
            <tr>
                <td style="background-color: {COLOR_HOCHNORMAL.name()};">Hochnormal</td>
                <td>130 bis 139</td>
                <td>85 bis 89</td>
            </tr>
            <tr>
                <td style="background-color: {COLOR_HYPERTONIE_GRAD_1.name()};">Hypertonie Grad 1</td>
                <td>140 bis 159</td>
                <td>90 bis 99</td>
            </tr>
            <tr>
                <td style="background-color: {COLOR_HYPERTONIE_GRAD_2.name()};">Hypertonie Grad 2</td>
                <td>160 bis 179</td>
                <td>100 bis 109</td>
            </tr>
            <tr>
                <td style="background-color: {COLOR_HYPERTONIE_GRAD_3.name()};">Hypertonie Grad 3</td>
                <td>180 oder mehr</td>
                <td>110 oder mehr</td>
            </tr>
            <tr>
                <td style="background-color: {COLOR_ISOLIERTE_HYPERTONIE.name()};">Isolierte systolische Hypertonie</td>
                <td>140 oder mehr</td>
                <td>unter 90</td>
            </tr>
        </tbody>
    </table>
    """

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auswertung")
        self.setGeometry(400, 400, 300, 250)
        self.db_manager = db_manager
        layout = QVBoxLayout(self)

        legend_label = QLabel()
        
        # HTML is used to color the text
        legend_label.setText(self.LEGEND_HTML)
        layout.addWidget(legend_label)

        self.days_combo = QComboBox()
        day_options = DaysOption.get_day_options()
        for label in day_options.keys():
            self.days_combo.addItem(label, day_options[label])
        layout.addWidget(self.days_combo)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Zeitstempel", "SYS", "DIA", "Puls"])
        layout.addWidget(self.table)

        self.days_combo.currentIndexChanged.connect(self.display_data)
        self.display_data()

        self.pdf_button = QPushButton("Exportieren als PDF")
        self.pdf_button.clicked.connect(self.export_pdf)
        layout.addWidget(self.pdf_button)

    def display_data(self):
        days = self.days_combo.currentData()
        rows = self.db_manager.fetch_filtered_data(days)

        self.table.setRowCount(0)
        for timestamp, sys, dia, pulse in rows:
            entry = BloodPressureEntry(timestamp, sys, dia, pulse)
            self.insert_row(entry)

    def insert_row(self, entry):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        color = self.get_row_color(entry.sys, entry.dia)
        self.table.setItem(row_position, 0, QTableWidgetItem(entry.timestamp))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(entry.sys)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(entry.dia)))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(entry.pulse)))
        self.apply_row_color(row_position, color)

    def apply_row_color(self, row_position, color):
        for col in range(4):
            self.table.item(row_position, col).setBackground(color)

    def get_row_color(self, sys, dia):
        if sys < 120 and dia < 80:
            return self.COLOR_OPTIMAL
        elif 120 <= sys <= 129 and 80 <= dia <= 84:
            return self.COLOR_NORMAL
        elif 130 <= sys <= 139 and 85 <= dia <= 89:
            return self.COLOR_HOCHNORMAL
        elif 140 <= sys <= 159 and 90 <= dia <= 99:
            return self.COLOR_HYPERTONIE_GRAD_1
        elif 160 <= sys <= 179 and 100 <= dia <= 109:
            return self.COLOR_HYPERTONIE_GRAD_2
        elif sys >= 180 and dia >= 110:
            return self.COLOR_HYPERTONIE_GRAD_3
        elif sys >= 140 and dia < 90:
            return self.COLOR_ISOLIERTE_HYPERTONIE
        else:
            return self.COLOR_DEFAULT

    
    def export_pdf(self):
        html_content = self.generate_html_content()
        document = QTextDocument()
        document.setHtml(html_content)
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("output/evaluation_report.pdf")
        document.print(printer)
        print("evaluation_report.pdf has been saved.")

    def generate_html_content(self):
            """Generates the HTML content for pdf export."""
            
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
                    {self.LEGEND_HTML}
                </div>
                <h2>Evaluation Report</h2>
                <table>
                    <tr>
                        <th>Zeitstempel</th>
                        <th>SYS</th>
                        <th>DIA</th>
                        <th>Puls</th>
                    </tr>
            """
            
            # Get the number of days from the selected combo box item
            days = self.days_combo.currentData()
            
            # Fetch filtered data based on the selected number of days
            rows = self.db_manager.fetch_filtered_data(days)

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