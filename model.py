from pydantic import BaseModel
from typing import Optional, List

class TagDetail(BaseModel):
  id: int = None
  url: str
  typ: str
  name: str

class TagType(BaseModel):
  id: int = None
  name: str
  color: str

class TagDetailList(BaseModel):
    all_tags: List[TagDetail]

