from datetime import datetime
from zoneinfo import ZoneInfo
import os

class DateZone:    
    TIMEZONE = os.getenv("TIMEZONE", "UTC")
    
    @staticmethod
    def get_timezone():
        return ZoneInfo(DateZone.TIMEZONE)

    @staticmethod
    def get_current_time():
        # Obtener la fecha y hora actual según la zona horaria configurada
        return datetime.now(DateZone.get_timezone())
