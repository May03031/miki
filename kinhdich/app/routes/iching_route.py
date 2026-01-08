from fastapi import APIRouter, Depends
from app.schemas.iching_schema import QuestionRequest
from app.db.models import User
from app.services import history_iching_service
from app.controller.iChing.ichingsession import IChingSession
from app.db.dependency import get_db
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.security import get_current_user
from app.services.history_iching_service import get_history
from app.schemas.info_schema import LimitRecord
from app.controller.iChing import PlumBlossomDivination, SerialDivination

router = APIRouter()


@router.post('/divine')
def divine(request: QuestionRequest,db: Session = Depends(get_db),  current_user: User = Depends(get_current_user)):
    sess = IChingSession.random(request.question)
    conv_his =get_history(db,current_user, LimitRecord())
    data = sess.summary(conv_his)
    history_iching_service.create_history(db,current_user, data)
    return data
    

@router.get('/history')
def history(db: Session = Depends(get_db),  current_user: User = Depends(get_current_user)):
    return history_iching_service.get_history(db, current_user)

@router.post("/api/maihua")
def maihua_api(request: QuestionRequest,db: Session = Depends(get_db),  current_user: User = Depends(get_current_user)):
    result = PlumBlossomDivination.from_datetime()
    return {"method": "mai_hua_dich_so", "result": result}

@router.post("/api/seri")
def seri_api(serial: str, request: QuestionRequest,db: Session = Depends(get_db),  current_user: User = Depends(get_current_user)):
    result = SerialDivination.from_serial(serial)
    return {"method": "seri_divination", "result": result}
