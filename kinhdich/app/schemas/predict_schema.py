from pydantic import BaseModel

class PredictRequest(BaseModel):
    value: float

class PredictResponse(BaseModel):
    result: float
