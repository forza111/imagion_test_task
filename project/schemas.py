from pydantic import BaseModel, HttpUrl

class Item(BaseModel):
    url: HttpUrl