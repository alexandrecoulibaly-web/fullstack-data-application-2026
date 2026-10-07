from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api_client import api_client
from app.templating import templates

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
def list_items(request: Request) -> HTMLResponse:
    items = api_client.list_items()
    return templates.TemplateResponse(request, "items/list.html", {"items": items})