from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from libraries.template import templates

router = APIRouter(tags=["index"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"gameid": "0001"}

    return templates.TemplateResponse(
        request=request, name="chatbox.jinja", context=context
    )
