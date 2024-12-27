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