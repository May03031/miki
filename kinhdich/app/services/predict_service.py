from app.models.predictor import Predictor

predictor = Predictor()

def get_prediction(value: float) -> float:
    return predictor.predict(value)
