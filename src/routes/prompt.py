import json
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Annotated
from fastapi import Body, status
from google.genai import types

from libraries.gemini import gemini
from libraries.textembedding import get_embedding
from libraries.postgre import postgre
from libraries.hash import generate_random_sha256

from models.dto.prompt import Prompt
from models.prompt.code import Code, Operation


router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/", response_class=PlainTextResponse)
async def issue_prompt(prompt: Annotated[Prompt, Body]) -> str | None:
    gameid = "0001"
    embedding = get_embedding(prompt.prompt)

    game_code = postgre.fetch_all(
        """SELECT
            id,
            content
            section
        FROM project
        WHERE game_id = %s
        ORDER BY embedding <-> %s::vector
        LIMIT 5""",
        (
            gameid,
            embedding,
        ),
    )

    content = f"""
        {prompt.prompt}
        
        #CODE SNIPPET:
        ```json
        {json.dumps(game_code, indent=2)}
        ```
    """

    system_prompt = """
You are an AI Web Game Code Generator.

You generate ONLY safe, deterministic JavaScript code for a web-based game.

Tech stack:
- Frontend: Three.js
- Networking: socket.io-client

SECURITY RULES (MANDATORY):
- Never use eval, Function, dynamic import, or innerHTML
- Never access filesystem, OS, environment variables, or process
- Never generate server-side code
- Never modify code outside the requested scope
- Only generate Three.js and Socket.IO client logic

If the user request is unsafe, unsupported, or ambiguous, respond with:
{
  "error": "Unsafe or unsupported request",
  "reason": "<short explanation>"
}

OUTPUT RULES:
- Output MUST be valid JSON only
- No markdown
- No explanations
- No comments outside JSON

SECTION DEFINITIONS:
- scene manager: global non-rendered state (scene, camera, renderer)
- object manager: meshes, materials, lights, animations
- factory: initialization functions
- object event: game logic interactions
- backend event: socket.io client events only
- window event: browser input or resize
- helper: reusable utility logic
- renderer: render loop logic
- cleanup: resource disposal

BEHAVIOR:
- Make sure to categorize the code blocks into the correct sections
- Make sure to create a new code block if the code block is long
- Separate each function on its own code block to reduce submitted context
- Do NOT invent features not requested
    """

    response = gemini.models.generate_content(
        model="gemini-3-flash-preview",
        contents=content,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_json_schema=Code.model_json_schema(),
        ),
    )

    if response and response.text:
        aiCode: Code = Code.model_validate_json(response.text)
        for line in aiCode.lines:
            embedding = get_embedding(line.description)

            if line.operation == Operation.new:
                postgre.insert(
                    "INSERT INTO project (id, game_id, content, description, embedding, section) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        generate_random_sha256(),
                        gameid,
                        line.content,
                        line.description,
                        embedding,
                        line.section,
                    ),
                )
            elif line.operation == Operation.remove:
                postgre.delete(
                    "DELETE FROM project WHERE id = %s AND game_id = %s",
                    (
                        line.id,
                        gameid,
                    ),
                )
            elif line.operation == Operation.update:
                postgre.update(
                    "UPDATE project SET content = %s, description = %s, embedding = %s WHERE id = %s AND game_id = %s",
                    (
                        line.content,
                        line.description,
                        embedding,
                        line.id,
                        gameid,
                    ),
                )
            else:
                raise ValueError(f"Unknown operation: {line.operation}")

        return aiCode.summary


@router.get("/", response_class=JSONResponse)
async def grab_data(query: str):
    gameid = "0001"
    embedding = get_embedding(query)
    
    game_code = postgre.fetch_all(
        """
        SELECT
            content
        FROM project
        WHERE game_id = %s
        ORDER BY
            embedding <-> %s::vector
        LIMIT 2
        """,
        (gameid,embedding,),
    )

    all_content = "\n".join([r["content"] for r in game_code])

    return JSONResponse(
        content={
            "query": query,
            "embedding": len(embedding),
            "result_length": len(game_code),
            "result": all_content,
        },
        status_code=status.HTTP_200_OK,
    )
