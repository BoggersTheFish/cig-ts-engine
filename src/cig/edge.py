from __future__ import annotations

from pydantic import BaseModel, Field


class Edge(BaseModel):
    """A weighted relation or constraint between two graph nodes."""

    id: str
    source: str
    target: str
    relation: str = "related"
    weight: float = Field(default=1.0, ge=-1.0, le=1.0)
    expected_target_activation: float | None = Field(default=None, ge=0.0, le=1.0)
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)

