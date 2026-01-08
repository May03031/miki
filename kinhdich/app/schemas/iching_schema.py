from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class iChingHistorySchema(BaseModel):
    user_id : int
    timestamp: str
    question: str
    coin_values: str
    original_name: str
    transformed_name: str
    original_meaning: str
    transformed_meaning: str