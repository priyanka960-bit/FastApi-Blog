from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi import Depends

from db.session import get_db
from db.models.users import Users
from apis.v1.route_login import get_current_user
from schemas.blog import ShowBlog, CreateBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_all_blogs, list_active_blogs, update_blog, list_inactive_blogs, delete_blog


router= APIRouter()

@router.post("/", response_model = ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session = Depends(get_db), current_user: Users=Depends(get_current_user)):
    blog = create_new_blog(blog=blog, db=db, author_id=current_user.id)
    return blog

@router.get("/{id}", response_model = ShowBlog, status_code=status.HTTP_200_OK)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog with ID {id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return blog

@router.get("/", response_model=List[ShowBlog])
def get_blogs(
    is_active: Optional[bool] = Query(
        None,
        description="true → active blogs, false → inactive blogs, omit → all blogs"
    ),
    db: Session = Depends(get_db)
):
    if is_active is True:
        return list_active_blogs(db)
    if is_active is False:
        return list_inactive_blogs(db)
    return list_all_blogs(db)


@router.put("/{id}", response_model=ShowBlog)
def update_a_blog(id: int, blog: UpdateBlog, db: Session=Depends(get_db), current_user: Users=Depends(get_current_user)):
    blog = update_blog(id=id, blog=blog, author_id=current_user.id, db=db)
    if isinstance(blog,dict):
        raise HTTPException(
            detail=blog.get("error"),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return blog

@router.delete("/{id}")
def delete_a_blog(id:int, db: Session = Depends(get_db), current_user: Users=Depends(get_current_user)):
    message = delete_blog(id=id, author_id=current_user.id, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"msg": f"Successfully deleted blog with id {id}"}