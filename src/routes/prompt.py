from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Annotated
from fastapi import Body, status
from datetime import datetime

# from libraries.gemini import gemini
from libraries.textembedding import get_embedding
from libraries.postgre import postgre

from models.dto.prompt import Prompt


router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/", response_class=PlainTextResponse)
async def issue_prompt(prompt: Annotated[Prompt, Body]) -> str | None:
    # response = gemini.models.generate_content(
    #     model="gemini-3-flash-preview",
    #     contents=prompt.prompt,
    # )

    # return response.text
    embedding = get_embedding(prompt.prompt)

    postgre.insert(
        "INSERT INTO game_0001 (content, description, topic, class, embedding, sort_index) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            prompt.prompt,
            "User provided a prompt: " + prompt.prompt,
            ["user", "prompt"],
            "prompt",
            embedding,
            datetime.now().timestamp(),
        ),
    )

    return prompt.prompt


@router.get("/", response_class=JSONResponse)
async def grab_data(query: str):
    embedding = get_embedding(query)

    result = postgre.fetch_all(
        """SELECT
            id,
            sort_index,
            content
        FROM game_0001
        ORDER BY embedding <-> %s::vector
        LIMIT 5""",
        (embedding, ),
    )
    
    result = sorted(result, key=lambda x: x['sort_index'])
    
    return JSONResponse(
        content={
            "query": query,
            "embedding": len(embedding),
            "result_length": len(result),
            "result": result,
        },
        status_code=status.HTTP_200_OK,
    )
