class BloodPressureEntry:
    """Data structure for storing a blood pressure entry."""
    def __init__(self, timestamp, sys, dia, pulse):
        self.timestamp = timestamp
        self.sys = sys
        self.dia = dia
        self.pulse = pulse