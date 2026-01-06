import io
from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google import genai
from os import getenv as env
from typing import Annotated
from pydantic import BaseModel, Field


class Prompt(BaseModel):
    prompt: str = Field(
        min_length=10,
        max_length=1000,
        description="Prompt for AI",
        examples=["create snake game"],
    )


app = FastAPI()

templates = Jinja2Templates(directory="templates")
gemini = genai.Client(api_key=env("AI_API_KEY"))

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"gameid": "0001"}

    return templates.TemplateResponse(
        request=request, name="chatbox.jinja", context=context
    )


@app.get("/preview/{gameid}", response_class=HTMLResponse)
async def preview(request: Request, gameid: str):
    context = {"gameid": gameid}

    return templates.TemplateResponse(
        request=request, name="preview.jinja", context=context
    )


@app.get("/gamescript/{gameid}", response_class=StreamingResponse)
async def gamescript(request: Request, gameid: str):
    file_content_str = io.StringIO(
        """
const width = window.innerWidth
const height = window.innerHeight
// Scene
const scene = new THREE.Scene()
scene.background = new THREE.Color('#00b140')
// Camera
const fov = 45 // AKA Field of View
const aspect = window.innerWidth / window.innerHeight
const near = 0.1 // the near clipping plane
const far = 100 // the far clipping plane
const camera = new THREE.PerspectiveCamera(fov, aspect, near, far)
camera.position.set(0, 0, 10)
// Renderer
const renderer = new THREE.WebGLRenderer()
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
// Creating a cube
const geometry = new THREE.SphereGeometry(2.5, 32, 16)
const material = new THREE.MeshBasicMaterial({ wireframe: false })
const cube = new THREE.Mesh(geometry, material)
scene.add(cube)
// Rendering the scene
const container = document.querySelector('#threejs-container')
container.append(renderer.domElement)
renderer.render(scene, camera)
"""
    )

    return StreamingResponse(file_content_str, media_type="text/javascript")


@app.post("/prompt", response_class=PlainTextResponse)
async def issue_prompt(prompt: Annotated[Prompt, Body]) -> str | None:
    response = gemini.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt.prompt,
    )

    return response.text
