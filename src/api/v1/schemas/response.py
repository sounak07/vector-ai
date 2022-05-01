from typing import Optional, List,Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: str

class SuccessResponse(BaseResponse):
    message: str

class SuccessResponseResults(BaseResponse):
    message: str
    data: Optional[dict]

