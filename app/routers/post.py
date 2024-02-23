from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import model, schemas, errors, utils, oauth2
from typing import Optional, List
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



''' 
##################################
CRUD OPERATIONS FOR POSTS MODULE
##################################
'''

# GET ALL POSTS 

@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   # posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(
            model.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return posts

# GET A SINGLE POST BY AN ID

@router.get("/{id}", response_model=schemas.PostOut)
def get_post_id(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(model.Post).filter(model.Post.id == id).first()
    post = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(
            model.Post.id).filter(model.Post.id == id).first()
    errors.post_not_found(post, id) # Check if post is not found and raise HTTPException 
    return post

# CREATE A POST 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    

    print(current_user.id) 
    new_post = model.Post(owner_id= current_user.id, **post.dict()) # **kwargs used.

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# DELETE A POST 

@router.delete("/{id}")
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    errors.post_not_found(post, id) # Check if post is not found and raise HTTPException 
    #post.delete(synchronize_session=False) #NOT WORKED
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorized to perform requested action")
    db.delete(post)  
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A POST 

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int,update_posts: schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    errors.post_not_found(post, id) # Check if post is not found and raise HTTPException 


    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorized to perform requested action")
    post_query.update(update_posts.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()