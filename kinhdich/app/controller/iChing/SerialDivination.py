from app.controller.iChing.line import Line
from app.controller.iChing.hexagram import Hexagram
import random

class SerialDivination:
    @staticmethod
    def from_serial(serial: str):
        digits = [int(ch) for ch in serial if ch.isdigit()]
        if len(digits) < 8:
            raise ValueError("Cần ít nhất 8 chữ số để gieo quẻ từ số seri")

        first8 = digits[:8]
        upper_sum = sum(first8[:4]) % 8 or 8
        lower_sum = sum(first8[4:]) % 8 or 8
        changing_line = sum(first8) % 6 or 6

        original_hex = Hexagram([Line(random.choice([6,7,8,9])) for _ in range(6)])
        changed_hex = original_hex.changed()

        return {
            "serial": serial,
            "digits": first8,
            "upper_trigram": upper_sum,
            "lower_trigram": lower_sum,
            "changing_line": changing_line,
            "original_hexagram": {
                "name": original_hex.name(),
                "binary_code": original_hex.to_binary_code(),
                "display": original_hex.display(),
                "meaning": original_hex.meaning()

            },
            "changed_hexagram": {
                "name": changed_hex.name(),
                "binary_code": changed_hex.to_binary_code(),
                "display": changed_hex.display(),
                "meaning": original_hex.meaning()
            }
        }