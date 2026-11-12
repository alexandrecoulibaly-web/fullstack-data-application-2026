from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BusinessError, ResourceNotFound
from app.routers.items import router as items_router

app = FastAPI(title="GearShare")


@app.exception_handler(BusinessError)
async def business_error_handler(
    request: Request, exc: BusinessError
) -> JSONResponse:
    status_code = 404 if isinstance(exc, ResourceNotFound) else 409
    return JSONResponse(status_code=status_code, content={"detail": exc.message})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(items_router)