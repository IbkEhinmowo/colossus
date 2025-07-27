from pydantic import BaseModel
from typing import Optional, List

class IncomingListing(BaseModel):
    listings: List[str]

class ParsedListing(BaseModel):
    title: str
    price: str
    location: str
    link: str
    is_just_listed: bool = False
