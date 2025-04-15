from datetime import datetime
from zoneinfo import ZoneInfo
import os
import time

class DateZone:
    TIMEZONE = os.getenv("TIMEZONE", "UTC")

    @staticmethod
    def get_timezone():
        return ZoneInfo(DateZone.TIMEZONE)

    @staticmethod
    def get_current_time():
        # Obtener la fecha y hora actual como Unix timestamp (entero)
        return int(time.time())
