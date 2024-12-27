from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui.easter_dialog import EasterDialog

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
