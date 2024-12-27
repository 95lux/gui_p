import datetime

def calculate_easter(year, orthodox=False):
    """Berechnet das Osterdatum für ein gegebenes Jahr."""
    
    year = int(year)
    if orthodox:
        # Griechisch-Orthodoxe Berechnung (Julianischer Kalender)
        a = year % 19
        b = year % 7
        c = year % 4
        d = (19 * a + 16) % 30
        e = (2 * c + 4 * b + 6 * d) % 7
        day = d + e + 3
        if day > 30:
            easter = datetime.date(year, 5, day - 30)
        else:
            easter = datetime.date(year, 4, day)
    else:
        # Christliche Berechnung (Gregorianischer Kalender)
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        easter = datetime.date(year, month, day)
    return easter


def get_holidays(easter):
    """Gibt Karfreitag, Ostersonntag und Ostermontag zurück."""
    good_friday = easter - datetime.timedelta(days=2)
    easter_monday = easter + datetime.timedelta(days=1)
    return good_friday, easter, easter_monday
