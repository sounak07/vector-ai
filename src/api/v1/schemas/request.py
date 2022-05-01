from typing import Optional, List
from pydantic import BaseModel


class UserInput(BaseModel):
    userFeeling: str

