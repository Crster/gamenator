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
        description=(
            "Identifier of the existing code snippet this operation applies to. "
            "Use the exact id previously provided by the system when updating or removing code. "
            "If and ONLY if the operation is 'new', set this value strictly to the string 'undefined'. "
            "Do NOT invent ids."
        ),
        example="undefined",
    )

    operation: Operation = Field(
        description=(
            "Defines the action to perform on the code snippet. "
            "'new' creates a brand-new snippet, "
            "'update' modifies an existing snippet identified by id, "
            "'remove' deletes an existing snippet identified by id. "
            "The operation must be logically consistent with the id field."
        ),
        example="new",
    )

    section: Section = Field(
        description=(
            "Specifies the logical section of the Three.js codebase this snippet belongs to. "
            "You MUST choose exactly one value from the Section enum. "
            "Do NOT invent new sections or reuse a section incorrectly. "
            "The section must accurately reflect the responsibility of the code."
        ),
        example="scene manager",
    )

    content: str = Field(
        description=(
            "Pure JavaScript code for this snippet only. "
            "Do NOT include explanations, markdown, JSON, comments outside the code itself, "
            "or unrelated logic. "
            "The code must be syntactically valid, readable, and limited to the responsibility "
            "described by the selected section."
        ),
        example="const scene = new THREE.Scene();",
    )

    description: str = Field(
        description=(
            "A concise, embedding-optimized explanation of the code snippet`s responsibility, "
            "scope, and usage context. "
            "This field MUST explicitly state: "
            "(1) the primary responsibility of the code, "
            "(2) the Three.js concepts involved (e.g., scene, camera, mesh, renderer, event, animation loop), "
            "(3) when or why this code should be modified or referenced, "
            "and (4) any assumptions or dependencies relevant to future edits. "
            "Write in complete sentences using clear technical terms. "
            "Avoid vague language, avoid repeating the code verbatim, "
            "and avoid mentioning line numbers or file structure."
        ),
        example=(
            "Creates and configures the main Three.js scene, including background color and "
            "global coordinate space. This snippet should be modified when adding environment-wide "
            "settings such as fog, background textures, or scene-level effects. "
            "It assumes the renderer and camera are initialized elsewhere."
        ),
    )


class Code(BaseModel):
    lines: list[CodeLine] = Field(
        description=(
            "An ordered list of CodeLine objects representing the complete set of changes "
            "to apply for the current user request. "
            "Each entry must be independent, valid, and collectively form a coherent solution. "
            "Do NOT omit required steps needed for the scene to work."
        ),
        example=[],
    )

    summary: str = Field(
        description=(
            "A short, commit-style summary describing the intent and impact of the code changes. "
            "The summary MUST start with a present-tense action verb (e.g., Add, Update, Remove, Refactor, Fix). "
            "It MUST describe the overall behavior or capability added, changed, or removed, "
            "not implementation details or individual lines of code. "
            "The summary should be understandable on its own when reviewing change history, "
            "and should clearly communicate what was changed and why at a high level."
        ),
        example="Add renderer initialization and animation loop for basic Three.js scene.",
    )
