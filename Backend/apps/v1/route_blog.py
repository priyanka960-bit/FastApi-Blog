from fastapi import APIRouter, Request, Depends, Form, responses, status
from typing import Optional
from sqlalchemy.orm import Session

from db.session import get_db
from db.repository.blog import (
    list_all_blogs,
    retrieve_blog,
    create_new_blog,
    delete_blog,
    update_blog,
)
from schemas.blog import CreateBlog, UpdateBlog
from apis.v1.route_login import get_current_user
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


# ---------- LIST ----------
@router.get("/")
def blog_list(request: Request, alert: Optional[str] = None, db: Session = Depends(get_db)):
    blogs = list_all_blogs(db=db)
    return templates.TemplateResponse(
        "blog/home.html",
        {"request": request, "blogs": blogs, "alert": alert},
    )


# ---------- CREATE ----------
@router.get("/create-new-blog")
def create_blog(request: Request):
    return templates.TemplateResponse(
        "blog/create_blog.html",
        {
            "request": request,
            "page_title": "Write a Blog",
            "heading": "Write a Blog",
            "button_text": "Submit for Review",
            "action_url": "/blogs/create-new-blog",
            "is_update": False,
            "blog": None,
            "title": "",
            "content": "",
            "errors": [],
        },
    )


@router.post("/create-new-blog")
def create_blog_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)

    try:
        author = get_current_user(token=token, db=db)

        blog = create_new_blog(
            blog=CreateBlog(title=title, content=content),
            db=db,
            author_id=author.id,
        )

        # 🔑 force refresh
        db.refresh(blog)

        return responses.RedirectResponse(
            f"/blogs/{blog.id}",
            status_code=status.HTTP_302_FOUND,
        )

    except Exception as e:
        print("Create failed:", e)
        return templates.TemplateResponse(
            "blog/create_blog.html",
            {
                "request": request,
                "errors": ["Please log in to create blog"],
                "title": title,
                "content": content,
            },
        )


# ---------- UPDATE ----------
@router.get("/update/{id}")
def update_blog_page(request: Request, id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        return responses.RedirectResponse(
            "/blogs?alert=Blog not found",
            status_code=status.HTTP_302_FOUND,
        )

    return templates.TemplateResponse(
        "blog/create_blog.html",
        {
            "request": request,
            "page_title": "Update Blog",
            "heading": "Update Blog",
            "button_text": "Update Blog",
            "action_url": f"/blogs/{id}",
            "is_update": True,
            "blog": blog,
            "title": blog.title,
            "content": blog.content,
            "errors": [],
        },
    )


@router.post("/{id}")
def update_blog_post(
    request: Request,
    id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)

    try:
        author = get_current_user(token=token, db=db)

        updated = update_blog(
            id=id,
            blog=UpdateBlog(title=title, content=content),
            author_id=author.id,
            db=db,
        )

        if isinstance(updated, dict) and updated.get("error"):
            raise Exception(updated["error"])

        db.refresh(updated)

        return responses.RedirectResponse(
            f"/blogs/{id}",
            status_code=status.HTTP_302_FOUND,
        )

    except Exception as e:
        print("Update failed:", e)
        return responses.RedirectResponse(
            f"/blogs/{id}?alert={e}",
            status_code=status.HTTP_302_FOUND,
        )


# ---------- DELETE ----------
@router.get("/delete/{id}")
def delete_a_blog(request: Request, id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)

    author = get_current_user(token=token, db=db)
    msg = delete_blog(id=id, author_id=author.id, db=db)

    alert = msg.get("error") or msg.get("msg")

    return responses.RedirectResponse(
        f"/blogs?alert={alert}",
        status_code=status.HTTP_302_FOUND,
    )


# ---------- DETAIL (KEEP LAST) ----------
@router.get("/{id}")
def blog_detail(request: Request, id: int, alert: Optional[str] = None, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)

    if not blog:
        return templates.TemplateResponse(
            "blog/detail.html",
            {
                "request": request,
                "blog": None,
                "alert": "Blog not found",
            },
        )

    return templates.TemplateResponse(
        "blog/detail.html",
        {"request": request, "blog": blog, "alert": alert},
    )
