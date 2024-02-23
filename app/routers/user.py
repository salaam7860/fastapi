from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import model, schemas, errors, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['Users']
)




''' 
##################################
CRUD OPERATIONS FOR USERS MODULE
##################################
'''

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

def create_user(user: schemas.UsersCreate, db: Session=Depends(get_db)):

    # hash the password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password # The idea is to replace the original plaintext password with its hashed version before storing it in the database.

    new_user = model.User(**user.dict()) # **kwargs used.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    errors.user_not_found(user, id) # Check if post is not found and raise HTTPException 

    return user