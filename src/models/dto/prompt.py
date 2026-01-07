from pydantic import BaseModel, Field


class Prompt(BaseModel):
    prompt: str = Field(
        min_length=3,
        max_length=255,
        description="Prompt for AI",
        examples=["create snake game"],
    )
