from __future__ import annotations

from collections import defaultdict

from agriPolaris.application.repository import SupplyRepository
from agriPolaris.domain.models import SupplyMatch, SupplyState
from agriPolaris.domain.priority_index import PriorityEntry, PriorityIndex
from agriPolaris.domain.validation import normalize_crop, normalize_lgu


class SupplyMonitorService:
    def __init__(self, repository: SupplyRepository) -> None:
        self._repository = repository
        self._indexes: dict[str, PriorityIndex] = defaultdict(PriorityIndex)

        self._repository.initialize()
        self._load_from_repository()

    def _load_from_repository(self) -> None:
        for record in self._repository.fetch_all():
            self._indexes[record.crop].upsert(record.lgu, record.priority)

    def upsert_supply(self, *, lgu: str, crop: str, current_supply: int, ideal_supply: int) -> SupplyState:
        normalized_lgu = normalize_lgu(lgu)
        normalized_crop = normalize_crop(crop)

        priority = int(current_supply) - int(ideal_supply)

        self._repository.upsert(crop=normalized_crop, lgu=normalized_lgu, priority=priority)
        self._indexes[normalized_crop].upsert(normalized_lgu, priority)

        return SupplyState(lgu=normalized_lgu, crop=normalized_crop, priority=priority)

    def list_supply(self) -> dict[str, list[SupplyState]]:
        result: dict[str, list[SupplyState]] = {}
        for crop, index in sorted(self._indexes.items()):
            states = [
                SupplyState(lgu=entry.lgu, crop=crop, priority=entry.priority)
                for entry in index.entries_sorted()
            ]
            result[crop] = states
        return result

    def get_crop_supply(self, crop: str) -> list[SupplyState]:
        normalized_crop = normalize_crop(crop)
        index = self._indexes.get(normalized_crop)
        if not index:
            return []

        return [
            SupplyState(lgu=entry.lgu, crop=normalized_crop, priority=entry.priority)
            for entry in index.entries_sorted()
        ]

    def get_most_critical(self, crop: str | None = None) -> SupplyState | None:
        if crop is not None:
            normalized_crop = normalize_crop(crop)
            index = self._indexes.get(normalized_crop)
            if not index:
                return None
            entry = index.most_critical()
            if not entry:
                return None
            return SupplyState(lgu=entry.lgu, crop=normalized_crop, priority=entry.priority)

        candidates: list[SupplyState] = []
        for crop_name, index in self._indexes.items():
            candidate = index.most_critical()
            if candidate:
                candidates.append(
                    SupplyState(lgu=candidate.lgu, crop=crop_name, priority=candidate.priority)
                )

        if not candidates:
            return None

        return max(candidates, key=lambda state: (abs(state.priority), state.priority))

    def match_supply(self, crop: str) -> SupplyMatch | None:
        normalized_crop = normalize_crop(crop)
        index = self._indexes.get(normalized_crop)
        if not index or len(index) < 2:
            return None

        shortage = index.top_shortage()
        oversupply = index.top_oversupply()

        if not shortage or not oversupply:
            return None

        if shortage.lgu == oversupply.lgu:
            return None

        return SupplyMatch(
            oversupply=SupplyState(
                lgu=oversupply.lgu,
                crop=normalized_crop,
                priority=oversupply.priority,
            ),
            shortage=SupplyState(
                lgu=shortage.lgu,
                crop=normalized_crop,
                priority=shortage.priority,
            ),
        )

    def flush(self) -> None:
        self._repository.clear()
        for index in self._indexes.values():
            index.clear()
        self._indexes.clear()
