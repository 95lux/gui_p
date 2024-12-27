# Blood Pressure Tracker

A PyQt5 application to log and evaluate blood pressure data using an SQLite database.

## Project Structure

- **`blood_pressure_entry.py`**  
  Defines the `BloodPressureEntry` datatype for representing blood pressure entries.

- **`database_manager.py`**  
  Handles database operations, including 
  - creating tables
  - adding entries
  - fetching filtered data (depending on the selected time period for data retrieval).

- **`days_option.py`**  
  Provides enum-like datatype, for filtering data by predefined time periods in the combobox.

- **`evaluation_dialog.py`**  
  Implements the evaluation dialog, displaying blood pressure data in a table with colored categories and PDF export feature. 
  PDF export generates HTML, which is used because of easy formatting and styling options. 
  `res/styles.css` contains CSS for this HTML

- **`main_window.py`**  
  Implements the main window with input fields for blood pressure values and buttons for submitting data and opening the evaluation dialog.

- **`main.py`**  
  Entry point of the application. Initializes the GUI.

## How to Run
1. Install the required dependencies (`PyQt5`, `sqlite3` is included with Python).
2. Run `main.py` from `a21` folder, to launch the application.
3. Use the main window to log blood pressure data and evaluate past entries.

