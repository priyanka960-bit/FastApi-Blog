from typing import Optional
from pydantic import BaseModel, model_validator
from datetime import datetime


class CreateBlog(BaseModel):
    title: str 
    slug: Optional[str] = None
    content: Optional[str] = None 
    
    @model_validator(mode="before")
    def generate_slug(cls, values):
        title = values.get("title")
        slug = values.get("slug")
        if title and not slug:
            values['slug'] = values.get("title").replace(" ","-").lower()
        return values

class UpdateBlog(CreateBlog):    
    pass
    

class ShowBlog(BaseModel):
    id: int
    title: str 
    content: Optional[str]
    created_at: datetime


    class Config():
        orm_mode = True