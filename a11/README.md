# Easter Festival Calculator

A PyQt5 application to calculate the dates for Easter and related holidays (Good Friday, Easter Sunday, and Easter Monday) based on the Christian or Orthodox calendars.

## Project Structure

- **`main.py`**  
  Entry point of the application. Initializes and runs the PyQt5 application.

- **`ui/easter_dialog.py`**  
  Implements the dialog for entering the year and selecting the calendar type (Christian or Orthodox) to calculate Easter and related holidays.

- **`ui/main_window.py`**  
  Implements the main window of the application, displaying an image and providing a menu to open the Easter calculation dialog.

- **`utils/easter_calculator.py`**  
    Contains the logic for calculating Easter and related holidays (Good Friday, Easter Sunday, Easter Monday) based on the selected calendar system (Christian or Orthodox). 
    Calculation is derived from the well-known easter algorithms 

    _Orthodox calculation algorithm derived from https://en.wikipedia.org/wiki/Date_of_Easter_  

    _Christian calculation algorithm (Gauss easter algorithm) derived from https://www.geeksforgeeks.org/how-to-calculate-the-easter-date-for-a-given-year-using-gauss-algorithm/_ 

## How to Run
1. Install the required dependencies (`PyQt5`).
2. Run `main.py` from the root of the `a11` folder, to launch the application.
3. Use the main window to select the calendar type and enter a year to calculate Easter and related holidays.
