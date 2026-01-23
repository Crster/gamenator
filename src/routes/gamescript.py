from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from libraries.postgre import postgre

router = APIRouter(prefix="/gamescript", tags=["index"])


@router.get("/{gameid}", response_class=StreamingResponse)
async def gamescript(gameid: str):
    game_code = postgre.fetch_all(
        """
        SELECT
            content
        FROM project
        WHERE game_id = %s
        ORDER BY
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
        """,
        (gameid,),
    )

    all_content = "\n".join([r["content"] for r in game_code])
    return StreamingResponse(all_content, media_type="text/javascript")
