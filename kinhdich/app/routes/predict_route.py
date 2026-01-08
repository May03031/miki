from fastapi import APIRouter, Depends
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.services.predict_service import get_prediction
from app.core.security import verify_token

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest, username: str = Depends(verify_token)):
    # username là người đang đăng nhập
    result = get_prediction(request.value)
    return PredictResponse(result=result)
