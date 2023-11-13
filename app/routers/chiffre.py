from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db
from .. import oauth2


router = APIRouter(tags=["Chiffres"])


# *********************GET users's all****************************************************************
@router.get("/historique-chiffres-affaire", response_model=List[schemas.Chiffre])
def get_chiffres(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    chiffres = (
        db.query(models.Chiffre)
        .filter(models.Chiffre.owner_id == current_user.id)
        .all()
    )
    return chiffres


# *********************POST*******************************************************************
@router.post(
    "/nouveau-chiffre-affaire",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Chiffre,
)
def create_chiffres(
    chiffre: schemas.ChiffreCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_chiffre = models.Chiffre(owner_id=current_user.id, **chiffre.dict())
    db.add(new_chiffre)
    db.commit()
    db.refresh(new_chiffre)

    return new_chiffre
