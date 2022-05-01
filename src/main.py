import uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status

from api.v1.api import api_router
from common.error import InvalidInput, NotFound
from services.sql_app import models
from services.sql_app.database import engine



app = FastAPI()

app = FastAPI(title="Vector", openapi_url="/api/v1/vector.json")
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
def init_db():
    models.Base.metadata.create_all(bind=engine)


@app.exception_handler(InvalidInput)
async def Invalid_input(request, exc: InvalidInput):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"{exc}"},
    )

@app.exception_handler(NotFound)
async def Invalid_input(request, exc: NotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc}"},
    )

@app.get("/")
async def root():
    return {"message": "Hello Vector, welcome to the future!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
