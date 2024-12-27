import sqlite3
from datetime import (datetime, timedelta)

class DatabaseManager:
    def __init__(self, db_path='db/blood_pressure.db'):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

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

    def add_entry(self, sys, dia, pulse):
        """Adds a new blood pressure entry to the database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO blood_pressure (timestamp, sys, dia, pulse)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, sys, dia, pulse))
        self.connection.commit()

    def fetch_filtered_data(self, days):
        """Fetches blood pressure data filtered by the number of days."""
        threshold_date = datetime.now() - timedelta(days=days)
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT timestamp, sys, dia, pulse
            FROM blood_pressure
            WHERE timestamp >= ?
        ''', (threshold_date.strftime("%Y-%m-%d %H:%M:%S"),))
        return cursor.fetchall()