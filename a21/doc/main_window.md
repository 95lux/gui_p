# File: `main_window.py`

## Description
This file defines the `MainWindow` class, which represents the main window of the application. It displays an image and provides a menu to open the Easter calculation dialog. The window is resizable and adjusts the image to maintain the aspect ratio when resized.

## **Classes**

### **`MainWindow`**
This class represents the main window of the Easter Festival Calculator application. It provides the interface for the user to select the calendar type and year to calculate Easter and related holidays. The window also displays an image and a menu bar.

#### **Methods**
- **`__init__(self)`**  
  Initializes the main window and sets up the UI.
  - Sets the window title to "Osterfestberechnung."
  - Loads and displays an image (`easter.jpg`) in the window.
  - Adds a menu bar with two menus: "Datei" (File) and "Ostern bestimmen" (Determine Easter).
  - Adds actions to the menus:
    - "Beenden" (Exit): Closes the application.
    - "Ostern bestimmen" (Determine Easter): Opens the Easter calculation dialog.
  - Resizes the window to fit the image and the menu bar.

- **`open_easter_dialog(self)`**  
  Opens the Easter dialog to allow the user to calculate Easter and related holidays.

- **`resizeEvent(self, event)`**  
  Adjusts the window size and image display when the window is resized.
  - Enforces the aspect ratio of the image by adjusting the height based on the new width.
  - Resizes and repositions the image (`pixmap`) to fit the new dimensions of the window.
  - Calls the parent class `resizeEvent` to ensure proper handling of the resize event.

## **Dependencies**
- **PyQt5 Modules**:
  - `QMainWindow`, `QAction`, `QVBoxLayout`, `QLabel`, `QWidget`: Used to create the window, layout, and UI components.
  - `QPixmap`: Used to load and display the image.
  - `Qt`: Provides the `Qt.KeepAspectRatio` constant for resizing the image while maintaining its aspect ratio.
- **Custom Modules**:
  - `EasterDialog` from `ui.easter_dialog`: Opens the dialog for calculating Easter dates.

## **Key Features**
1. **Resizable Window**  
   The window automatically resizes based on the window's dimensions, ensuring that the image retains its aspect ratio.

2. **Menu Bar**  
   The menu bar provides two options:
   - **Beenden**: Exits the application.
   - **Ostern bestimmen**: Opens a dialog to calculate the Easter dates.

3. **Image Display**  
   Displays an image (`easter.jpg`) in the main window, which is resized to fit the window while maintaining its aspect ratio.

4. **Easter Calculation**  
   Allows users to open a dialog to determine Easter and related holidays for a given year and calendar type (Christian or Orthodox).

## **How It Works**
1. The main window displays an image and a menu bar with actions.
2. The user can click "Ostern bestimmen" to open the dialog to calculate Easter.
3. The window automatically adjusts the size of the displayed image when resized, ensuring the aspect ratio remains consistent.

