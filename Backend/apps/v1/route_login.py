import json
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.users import UserCreate
from db.repository.user import create_new_user
from apis.v1.route_login import get_current_user
from apis.v1.route_login import authenticate_user
from core.security import create_access_token
from pydantic.error_wrappers import ValidationError
from fastapi.security.utils import get_authorization_scheme_param

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/signup")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html",{"request":request})

@router.post("/signup")
def register(request: Request, email: str = Form(...), password: str= Form(...), db: Session = Depends(get_db)):
    errors = []
    try:
        user = UserCreate(email=email,password=password)
        create_new_user(user=user, db=db)
        return responses.RedirectResponse("/?alert=Successfully%20Registered",status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        errors_list = json.loads(e.json())
        for item in errors_list:
            errors.append(item.get("loc")[0]+ ": " + item.get("msg"))
        return templates.TemplateResponse("auth/register.html",{"request":request,"errors":errors})
    
@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
def login(request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    errors = []
    user = authenticate_user(email=email,password=password,db=db)
    if not user:
        errors.append("Incorrect email or password")
        return templates.TemplateResponse("auth/login.html", {"request": request,"errors":errors})
    access_token = create_access_token(data={"sub": email})
    response = responses.RedirectResponse(
            "/blogs?alert=Successfully Logged In", status_code=status.HTTP_302_FOUND
        )
    response.set_cookie(key="access_token",value=f"Bearer {access_token}",httponly=True)
    return response

@router.get("/logout")
def logout():
    response = responses.RedirectResponse(
        url="/auth/login",
        status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("access_token")
    return response

@router.get("/profile")
def profile(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)

    user = get_current_user(token=token, db=db)

    return templates.TemplateResponse(
        "auth/profile.html",
        {
            "request": request,
            "user": user
        }
    )


    
