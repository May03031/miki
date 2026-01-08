from fastapi import FastAPI
from app.routes.auth_route import router as auth_router
from app.routes.predict_route import router as predict_router
from app.routes.iching_route import router as iching_route
from app.db.database import Base, engine

# tạo database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Backend with FastAPI + PyTorch + JWT")

# gắn router
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(predict_router, prefix="/api", tags=["Prediction"])
app.include_router(iching_route, prefix="/api/iching", tags=["Iching"])
@app.get("/")
def home():
    return {"message": "Welcome to AI Backend with JWT"}
