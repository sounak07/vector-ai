from fastapi import APIRouter, status, HTTPException
from api.v1.schemas import SuccessResponse
from libs.response import response_out

router = APIRouter()


@router.get("", response_model=SuccessResponse)
async def health():
    return response_out("healthy", status.HTTP_200_OK)
