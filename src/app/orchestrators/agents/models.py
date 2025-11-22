from pydantic import BaseModel, Field


class ProductOwnerInput(BaseModel):
    requirement: str = Field(..., description="Raw feature request or user story.")


class ProductOwnerOutput(BaseModel):
    story: str
    acceptance_criteria: list[str]
    tasks: list[str]


class DeveloperInput(BaseModel):
    story: str
    acceptance_criteria: list[str]
    tasks: list[str]


class DeveloperOutput(BaseModel):
    summary: str = "Developer agent placeholder output"
