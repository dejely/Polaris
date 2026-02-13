from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class RepositoryRecord:
    crop: str
    lgu: str
    priority: int


class SupplyRepository(Protocol):
    def initialize(self) -> None:
        ...

    def upsert(self, *, crop: str, lgu: str, priority: int) -> None:
        ...

    def fetch_all(self) -> Iterable[RepositoryRecord]:
        ...

    def clear(self) -> None:
        ...
