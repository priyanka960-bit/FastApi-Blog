from apps.v1 import route_blog
from apps.v1 import route_login
from apps.v1 import home
from fastapi import APIRouter


app_router = APIRouter()

app_router.include_router(
    route_blog.router, prefix="/blogs", tags=[""], include_in_schema=False
)
app_router.include_router(
    route_login.router, prefix="/auth", tags=[""], include_in_schema=False
)
app_router.include_router(home.router)