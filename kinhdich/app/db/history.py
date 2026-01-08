from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class HistoryIching(Base):
    __tablename__ = "history_iching"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    question: Mapped[str] = mapped_column(String)
    timestamp: Mapped[str] = mapped_column(String)
    coin_values: Mapped[str] = mapped_column(String)
    original_name: Mapped[str] = mapped_column(String)
    transformed_name: Mapped[str] = mapped_column(String)
    original_meaning: Mapped[str] = mapped_column(String)
    transformed_meaning: Mapped[str] = mapped_column(String)
    

    