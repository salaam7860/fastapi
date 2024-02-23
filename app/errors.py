from fastapi import HTTPException
from starlette import status

# Check if post is not found and raise HTTPException 
def post_not_found(post, id):
       if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found") 


def user_not_found(user: int, id: int):
       if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found") 
    