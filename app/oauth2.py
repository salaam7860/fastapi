from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas, database, model
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # PICK THE URL FROM THE ROUTES 

# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# CREATE A TOKEN
def create_token(data: dict):
    to_encode = data.copy()

    # CREATE TIME EXPIRATION 
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # CREATE JWT TOKEN #### DATA, ALGORITHM AND SECRET KEY 
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token

# VERIFY THE ACCESS TOKEN 

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get("user_id")) # GET THE USER ID FROM auth.login.access_token

        if id is None:
            raise credentials_exception
        
        # VERIFY THE TOKEN DATA FROM THE SCHEMA 
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str= Depends(oauth2_scheme), db: Session= Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user