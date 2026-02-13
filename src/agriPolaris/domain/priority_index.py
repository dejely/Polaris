from __future__ import annotations

import heapq
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PriorityEntry:
    lgu: str
    priority: int


class PriorityIndex:
    """Update-safe dual-heap index for quick shortage/oversupply lookups."""

    def __init__(self) -> None:
        self._latest: dict[str, int] = {}
        self._min_heap: list[tuple[int, str]] = []
        self._max_heap: list[tuple[int, str]] = []

    def __len__(self) -> int:
        return len(self._latest)

    def upsert(self, lgu: str, priority: int) -> None:
        self._latest[lgu] = priority
        heapq.heappush(self._min_heap, (priority, lgu))
        heapq.heappush(self._max_heap, (-priority, lgu))

    def clear(self) -> None:
        self._latest.clear()
        self._min_heap.clear()
        self._max_heap.clear()

    def entries_sorted(self) -> list[PriorityEntry]:
        return [
            PriorityEntry(lgu=lgu, priority=priority)
            for lgu, priority in sorted(self._latest.items(), key=lambda pair: pair[1])
        ]

    def top_shortage(self) -> PriorityEntry | None:
        self._prune_min_heap()
        if not self._min_heap:
            return None
        priority, lgu = self._min_heap[0]
        if priority >= 0:
            return None
        return PriorityEntry(lgu=lgu, priority=priority)

    def top_oversupply(self) -> PriorityEntry | None:
        self._prune_max_heap()
        if not self._max_heap:
            return None
        neg_priority, lgu = self._max_heap[0]
        priority = -neg_priority
        if priority <= 0:
            return None
        return PriorityEntry(lgu=lgu, priority=priority)

    def most_critical(self) -> PriorityEntry | None:
        if not self._latest:
            return None

        lgu, priority = max(
            self._latest.items(),
            key=lambda pair: (abs(pair[1]), pair[1]),
        )
        return PriorityEntry(lgu=lgu, priority=priority)

    def _prune_min_heap(self) -> None:
        while self._min_heap:
            priority, lgu = self._min_heap[0]
            if self._latest.get(lgu) == priority:
                return
            heapq.heappop(self._min_heap)

    def _prune_max_heap(self) -> None:
        while self._max_heap:
            neg_priority, lgu = self._max_heap[0]
            if self._latest.get(lgu) == -neg_priority:
                return
            heapq.heappop(self._max_heap)
