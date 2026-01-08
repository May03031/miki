from datetime import datetime, timedelta
from typing import List, Optional
from app.controller.iChing.line import Line
from app.controller.iChing.hexagram import Hexagram
import random

class PlumBlossomDivination:
    @staticmethod
    def from_datetime(dt: Optional[datetime] = None):
        dt = dt or datetime.now()
        year, month, day, hour, minute = dt.year, dt.month, dt.day, dt.hour, dt.minute

        upper = (year + month + day) % 8 or 8
        lower = (year + month + day + hour) % 8 or 8
        moving = (year + month + day + hour + minute) % 6 or 6

        original_hex = Hexagram([Line(random.choice([6,7,8,9])) for _ in range(6)])
        changed_hex = original_hex.changed()

        return {
            "datetime": dt.isoformat(),
            "upper_trigram": upper,
            "lower_trigram": lower,
            "changing_line": moving,
            "original_hexagram": {
                "name": original_hex.name(),
                "binary_code": original_hex.to_binary_code(),
                "display": original_hex.display()
            },
            "changed_hexagram": {
                "name": changed_hex.name(),
                "binary_code": changed_hex.to_binary_code(),
                "display": changed_hex.display()
            }
        }