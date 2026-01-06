from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.prompt import router as PromptRouter
from routes.preview import router as PreviewRouter
from routes.gamescript import router as GameScriptRouter
from routes.index import router as IndexRouter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(PromptRouter)
app.include_router(PreviewRouter)
app.include_router(GameScriptRouter)
app.include_router(IndexRouter)
