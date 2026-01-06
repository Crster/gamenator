from pydantic import BaseModel, Field


class Prompt(BaseModel):
    prompt: str = Field(
        min_length=10,
        max_length=1000,
        description="Prompt for AI",
        examples=["create snake game"],
    )
