import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from api.v1.api import api_router
from common.error import InvalidInput


app = FastAPI()

app = FastAPI(title="SimBa", openapi_url="/api/v1/vector.json")
app.include_router(api_router, prefix="/api/v1")

# @app.exception_handler(InvalidInput)
# async def Ip_Error_Handler(request, exc: InvalidInput):
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content={"message": f"Oops! {exc} did something. There goes a rainbow..."},
#     )


@app.get("/")
async def root():
    return {"message": "Hello Vector, welcome to the future!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
