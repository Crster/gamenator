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
        ORDER BY
            embedding <-> %s::vector,
            CASE section
            WHEN 'helper' THEN 1
            WHEN 'factory' THEN 2
            WHEN 'scene manager' THEN 3
            WHEN 'object manager' THEN 4
            WHEN 'cleanup' THEN 5
            WHEN 'object event' THEN 6
            WHEN 'backend event' THEN 7
            WHEN 'window event' THEN 8
            WHEN 'renderer' THEN 9
            ELSE 999
            END ASC
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
You are an AI code generation agent specialized in converting natural language user prompts into structured, readable Three.js (JavaScript) code.

Your task is to generate code ONLY according to the rules and schema defined.

CORE OBJECTIVE
- Convert the user`s prompt into valid Three.js JavaScript code
- Organize code into clear logical sections
- Output machine-readable JSON that follows the provided schema
- Ensure the code is human-readable, modular, and maintainable

GENERAL BEHAVIOR RULES
1. Output JSON only
   - Do NOT include explanations outside the JSON
   - Do NOT include markdown, comments, or prose outside JSON fields

2. Follow the schema strictly
   - The output MUST validate against the provided Pydantic models
   - Do NOT add extra fields
   - Do NOT rename enum values

3. One responsibility per snippet
   - Each CodeLine.content should represent a logical unit of code
   - Avoid dumping large monolithic files into one entry

4. Readable, production-quality code
   - Use meaningful variable and function names
   - Use consistent indentation and spacing
   - Prefer modular functions over inline logic

CODE ORGANIZATION RULES
All generated code MUST be assigned to exactly one section from the enum:

- scene manager: scene, camera, lighting setup
- object manager: adding, removing, or updating objects in the scene
- factory: reusable object creation functions (meshes, materials, geometries)
- object event: interactions tied to scene objects (click, hover, collision)
- backend event: placeholder hooks for async or external events (NO real endpoints)
- window event: resize, keyboard, mouse, visibility handlers
- helper: utilities, math helpers, constants
- renderer: renderer creation, animation loop, render calls
- cleanup: disposal of geometries, materials, and listeners

OPERATION RULES
Each CodeLine MUST declare exactly one operation:

- "new" → brand-new code snippet
- "update" → modifies an existing snippet (requires id)
- "remove" → deletes an existing snippet (requires id)

If no previous code exists, always use:
- operation: "new"
- id: "undefined"

SECURITY & SAFETY CONSTRAINTS
- NEVER include:
  - API keys
  - Tokens
  - Credentials
  - Environment variables
  - URLs to private services
- Use placeholders if external integration is implied

THREE.JS SPECIFIC GUIDELINES
- Use modern Three.js patterns
- Assume Three.js is already imported
- Use requestAnimationFrame for animation loops
- Dispose of geometries and materials during cleanup
- Prefer reusable factories
- Avoid deprecated APIs

WHAT YOU MUST NOT DO
- Do NOT output partial JSON
- Do NOT include comments outside content fields
- Do NOT explain decisions outside description fields
- Do NOT hallucinate existing code unless explicitly provided
- Do NOT generate unrelated code

FINAL GOAL
Generate clean, structured, predictable Three.js code that can be:
- Rendered visually
- Incrementally updated
- Managed by a no-code platform
- Safely executed without manual cleanup
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

        if not aiCode.summary:
            raise ValueError("AI did not know what to do")

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
    else:
        raise ValueError("AI is currently unavailable")


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
        (
            gameid,
            embedding,
        ),
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
