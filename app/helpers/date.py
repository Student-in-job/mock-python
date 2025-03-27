from datetime import datetime, timedelta


class MonthDays:
    JANUARY: int = 31
    FEBRUARY: int = 29
    MARCH: int = 31
    APRIL: int = 30
    MAY: int = 31
    JUNE: int = 30
    JULY: int = 31
    AUGUST: int = 31
    SEPTEMBER: int = 30
    OCTOBER: int = 31
    NOVEMBER: int = 30
    DECEMBER: int = 31


class DatesUtils:
    @staticmethod
    def start_of_month(date: datetime) -> datetime:
        return datetime(date.year, date.month, 1)

    @staticmethod
    def middle_of_month(date: datetime) -> datetime:
        return datetime(date.year, date.month, 15)

    @staticmethod
    def next_month(date: datetime) -> datetime:
        days_to_add = {
            1: MonthDays.JANUARY,
            2: MonthDays.FEBRUARY,
            3: MonthDays.MARCH,
            4: MonthDays.APRIL,
            5: MonthDays.MAY,
            6: MonthDays.JUNE,
            7: MonthDays.JULY,
            8: MonthDays.AUGUST,
            9: MonthDays.SEPTEMBER,
            10: MonthDays.OCTOBER,
            11: MonthDays.NOVEMBER,
            12: MonthDays.DECEMBER
        }
        result = date + timedelta(days_to_add[date.month])
        return result

    @staticmethod
    def start_date(date: datetime, day: int) -> datetime:
        result = DatesUtils.middle_of_month(date) if (day > 20) else DatesUtils.start_of_month(date)
        return result
