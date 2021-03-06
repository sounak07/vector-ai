from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: str

class SuccessResponse(BaseResponse):
    message: str
    data: Optional[dict]

