from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def create_and_commit(db: Session, model, obj_data):
    try:
        obj = model(**obj_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail="Object already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))