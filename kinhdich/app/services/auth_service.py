from sqlalchemy.orm import Session
from app.db import models
from app.core.security import hash_password, verify_password, create_access_token
from app.db.dependency import get_db
from app.db.database import engine
#from sqlmodel import Field, SQLModel, create_engine, Session, select

def create_user(db: Session, username: str, password: str):
    hashed_pw = hash_password(password)
    new_user = models.User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user: models.User):
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"} 

def get_user(username: str):
    with Session(engine) as db:
        user = db.query(models.User).filter(models.User.username == username).first()
        return user

#from sqlmodel import Field, SQLModel, create_engine, Session, select
#def get_user(username: str) -> Optional[User]:
#   with Session(engine) as db:
#       return db.exec(select(User).where(User.username == username)).first()


