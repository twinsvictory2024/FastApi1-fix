from pydantic import BaseModel, Field
from typing import Annotated

import datetime

class AdCreate( BaseModel ):
    title: str
    description: str
    price: float = Field( gt=0 )
    author: str


class AdResponse( BaseModel ):
    id: int
    created_at: datetime.datetime
    title: str
    description: str
    price: float
    author: str


class AdUpdate( BaseModel ):
    title: str | None = None
    description: str | None = None
    price: float | None = Field( gt=0, default=None )