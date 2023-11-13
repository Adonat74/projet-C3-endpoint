from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db
from .. import oauth2

router = APIRouter(tags=["Users"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/user/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user


@router.put("/user-update/{id}", response_model=schemas.UserOut)
def update_user(
    id: int,
    updated_user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    hashed_password = utils.hash(updated_user.password)
    updated_user.password = hashed_password

    user = db.query(models.User).filter(models.User.id == id)

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    user.update(updated_user.dict(), synchronize_session=False)

    db.commit()

    return user.first()
