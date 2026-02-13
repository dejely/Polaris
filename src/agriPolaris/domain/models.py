from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SupplyState:
    lgu: str
    crop: str
    priority: int

    @property
    def status(self) -> str:
        if self.priority > 0:
            return "oversupply"
        if self.priority < 0:
            return "shortage"
        return "balanced"


@dataclass(frozen=True, slots=True)
class SupplyMatch:
    oversupply: SupplyState
    shortage: SupplyState
