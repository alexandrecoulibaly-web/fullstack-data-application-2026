from fastapi import FastAPI

from app.routers import items

app = FastAPI(title="GearShare API", version="0.1.0")
app.include_router(items.router)


@app.get("/health", tags=["monitoring"])
def health():
    return {"status": "ok"}
