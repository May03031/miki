from app.controller.iChing.hexagram import Hexagram
from datetime import datetime
from typing import List, Dict, Any
from app.db.history import HistoryIching
from config import settings



class IChingSession:
    def __init__(self, hexagram: Hexagram, question: str):
        self.original = hexagram
        self.changed_hex = hexagram.changed()
        self.timestamp = datetime.utcnow()
        self.question = question
    @classmethod
    def random(cls, question: str):
        hexagram = Hexagram.random()
        return cls(hexagram, question)
    
    def summary(self,  history: List[HistoryIching]):

        history = str
        if settings.AI_AGENT.lower().strip() == "gemini":
            history = [
                {"role": role, "parts": [{"text": text}]}
                for r in reversed(history)
                for role, text in [
                    ("user", r.question),
                    ("model", r.original_meaning)
                ] if text
            ]
        elif settings.AI_AGENT.lower().strip() == "openai":
             
            history = [
                {"role": role, "content": text}
                for r in reversed(history)
                for role, text in [
                    ("user", r.question),
                    ("assistant", r.original_meaning)
                ]
                if text  # bỏ qua nếu None hoặc rỗng
            ]

        
        coin_details = [l.toss_detail for l in self.original.lines]
        original_meaning = self.original.meaning(self.question, history)
        changing_lines = [i+1 for i,l in enumerate(self.original.lines) if l.changing]
        transformed_meaning = ""
        if not changing_lines:
            transformed_meaning = original_meaning
        else:
            transformed_meaning =  self.changed_hex.meaning(self.question, history)

        return {
            "question": self.question,
            "coin_details": coin_details,  # thêm chi tiết sấp ngửa
            "coin_values": [l.value for l in self.original.lines],
            "original_display": self.original.display(),
            "original_code": self.original.to_binary_code(),
            "original_name": self.original.name(),
            "original_meaning": original_meaning,
            "changing_lines": changing_lines,
            "transformed_display": self.changed_hex.display(),
            "transformed_code": self.changed_hex.to_binary_code(),
            "transformed_name": self.changed_hex.name(),
            "transformed_meaning": transformed_meaning,
            "timestamp": self.timestamp.isoformat() + 'Z'
        }
