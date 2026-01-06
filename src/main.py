from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(root_path="/src")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"gameid": "0001"}

    return templates.TemplateResponse(
        request=request, name="chatbox.jinja", context=context
    )


@app.get("/preview/{gameid}", response_class=HTMLResponse)
async def preview(request: Request, gameid: str):
    return f"Hello {gameid}"
