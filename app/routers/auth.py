from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from .. import database, schemas, model, utils, oauth2

router = APIRouter(tags=["Authencation"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:schemas.UserLogin, db: Session=Depends(database.get_db)):

    # VERIFY THE USER PROVIDED EMAIL AND PASSWORD WITH THE DATABASE 
    user = db.query(model.User).filter(model.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    ########## CREATE TOKEN ##########
    access_token = oauth2.create_token(data={"user_id": user.id})
    # RETURN TOKEN      
    return {"access_token": access_token, "token_type": "bearer"}


