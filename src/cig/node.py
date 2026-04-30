from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class NodeKind(StrEnum):
    """Supported TS node categories."""

    CONCEPT = "concept"
    CLAIM = "claim"
    SYMBOL = "symbol"
    MEMORY = "memory"
    STATE = "state"


class Node(BaseModel):
    """A concept, claim, symbol, memory, or state in the graph."""

    id: str
    label: str | None = None
    kind: NodeKind = NodeKind.CONCEPT
    activation: float = Field(default=0.0, ge=0.0, le=1.0)
    context: str | None = None
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)

    @property
    def display_label(self) -> str:
        return self.label or self.id

