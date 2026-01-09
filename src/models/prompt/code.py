from enum import Enum
from pydantic import BaseModel, Field


class Operation(str, Enum):
    update = "update"
    new = "new"
    remove = "remove"


class Section(str, Enum):
    scene_manager = "scene manager"
    object_manager = "object manager"
    factory = "factory"
    object_event = "object event"
    backend_event = "backend event"
    window_event = "window event"
    helper = "helper"
    renderer = "renderer"
    cleanup = "cleanup"


class CodeLine(BaseModel):
    id: str = Field(
        description="The id of the previous code snippet or undefined if adding a new snippet",
        example="sha256",
    )
    operation: Operation = Field(
        description="What operation to perform based on the provided code snippet",
        example=["new"],
    )
    section: Section = Field(
        description="The section of the game code to be updated",
        example=["scene manager"],
    )
    content: str = Field(
        description="The new or updated code snippet",
        example="console.log('Hello World!');",
    )
    description: str = Field(
        description="A detailed description of the code snippet",
        example="Prints 'Hello World!' to the console",
    )


class Code(BaseModel):
    lines: list[CodeLine] = Field(
        description="The whole code to be inserted or updated including the provided code",
        example=[],
    )
    summary: str = Field(
        description="A short summary of the changes made to the code",
        example=["Added a console.log statement to the code"],
    )
