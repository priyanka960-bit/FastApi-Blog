from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def landing(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {"request": request}
    )
