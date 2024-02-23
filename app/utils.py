from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# VERIFY THE USER PROVIDED PASSWORD WITH OUR DATABASE BY MAKING USER PROVIDED PASSWORD INTO HASH THEN COMPARE IT OURS.

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)