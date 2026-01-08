from typing import List, Optional

class Line:
    def __init__(self, value: int, toss_detail: Optional[List[int]] = None):
        if value not in (6,7,8,9):
            raise ValueError("Line must be 6,7,8,9")
        self.value = value
        self.changing = value in (6,9)
        self.yang = value in (7,9)
        self.toss_detail = toss_detail or []  # lưu kết quả 3 đồng xu
    def to_bit(self):
        return 1 if self.yang else 0
    def after_change(self):
        if self.value == 6: return Line(7)
        if self.value == 9: return Line(8)
        return Line(self.value)
    def symbol(self):
        return "———" if self.yang else "- -"