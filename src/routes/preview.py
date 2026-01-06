from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from libraries.template import templates

router = APIRouter(prefix="/preview", tags=["preview"])


@router.get("/{gameid}", response_class=HTMLResponse)
async def preview(request: Request, gameid: str):
    context = {"gameid": gameid}

    return templates.TemplateResponse(
        request=request, name="preview.jinja", context=context
    )
