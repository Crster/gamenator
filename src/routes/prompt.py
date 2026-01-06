from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from typing import Annotated
from fastapi import Body
from libraries.gemini import gemini

from models.dto.prompt import Prompt


router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/", response_class=PlainTextResponse)
async def issue_prompt(prompt: Annotated[Prompt, Body]) -> str | None:
    response = gemini.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt.prompt,
    )

    return response.text
