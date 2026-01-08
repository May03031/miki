from sqlalchemy.orm import Session
from app.db.history import HistoryIching
from app.schemas.iching_schema import iChingHistorySchema
from app.db.models import User
from sqlalchemy import select
from app.schemas.info_schema import LimitRecord

def create_history(db: Session,current_user: User, result: iChingHistorySchema):

    h = HistoryIching(
        user_id=current_user.id,
        timestamp=result['timestamp'],
        question = result['question'],
        coin_values=','.join(map(str, result['coin_values'])),
        original_name=result['original_name'],
        transformed_name=result['transformed_name'],
        original_meaning=result['original_meaning'],
        transformed_meaning=result['transformed_meaning']
    )
    db.add(h)
    db.commit()
    return result

def get_history(db: Session,current_user: User,):
    rows = db.exec(select(HistoryIching).where(HistoryIching.user_id==current_user.id).order_by(HistoryIching.id.desc())).all()
    return [r.__dict__ for r in rows]

def get_history(db: Session, current_user: User, rc: LimitRecord):

    stmt = (
        select(HistoryIching)
            .where(HistoryIching.user_id == current_user.id)
            .order_by(HistoryIching.id.desc())
            .offset(rc.offset)   
            .limit(rc.limit)  
    )

    result = db.execute(stmt).scalars().all()  # 👈 lấy list các object HistoryIching
    #return [r.__dict__ for r in result]
    return result

    




