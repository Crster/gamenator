import io
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/gamescript", tags=["index"])


@router.get("/{gameid}", response_class=StreamingResponse)
async def gamescript(request: Request, gameid: str):
    file_content_str = io.StringIO(
        """
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

// Creating a sphere
const geometry = new THREE.SphereGeometry(2.5, 32, 16)
const material = new THREE.MeshBasicMaterial({ wireframe: false })
const sphere = new THREE.Mesh(geometry, material)

// Scene
const scene = new THREE.Scene()
scene.background = new THREE.Color('#00b140')
scene.add(sphere)

// Rendering the scene
const container = document.querySelector('#threejs-container')
container.append(renderer.domElement)
renderer.render(scene, camera)
"""
    )

    return StreamingResponse(file_content_str, media_type="text/javascript")
