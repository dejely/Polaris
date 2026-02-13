from __future__ import annotations

from agriPolaris.application.service import SupplyMonitorService
from agriPolaris.infrastructure.sqlite_repository import SQLiteSupplyRepository

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


class SupplyMonitor:
    """Backward-compatible facade over the new service architecture."""

    def __init__(self, use_sorted: bool = True, db_name: str = "entries.db") -> None:
        del use_sorted
        self.db_name = db_name
        self._service = SupplyMonitorService(SQLiteSupplyRepository(db_path=self.db_name))

    def setup_db(self) -> None:
        self._service = SupplyMonitorService(SQLiteSupplyRepository(db_path=self.db_name))

    def create_crop_table(self, crop: str) -> None:
        # No-op in normalized schema. Kept for backward compatibility.
        del crop

    def flush_db(self) -> None:
        self._service.flush()

    def load_db(self) -> None:
        self._service = SupplyMonitorService(SQLiteSupplyRepository(db_path=self.db_name))

    def supply_checker(self, _lgu: str, crop: str, curr_supply: int, ideal_supply: int):
        return self._service.upsert_supply(
            lgu=_lgu,
            crop=crop,
            current_supply=curr_supply,
            ideal_supply=ideal_supply,
        )

    def remove_max(self):
        critical = self._service.get_most_critical()
        if not critical:
            return None
        return critical.lgu, critical.crop, critical.priority

    def get_most_critical_LGU(self):
        critical = self._service.get_most_critical()
        if not critical:
            return None
        return critical.lgu

    def show_pq(self) -> None:
        print("\n=== Priority Queues by Crop ===")
        all_supply = self._service.list_supply()
        if not all_supply:
            print("No records found.")
            return

        for crop, states in all_supply.items():
            print(f"\nCrop: {YELLOW}{crop}{RESET}")
            for state in states:
                print(
                    f"  LGU: {GREEN}{state.lgu}{RESET} | "
                    f"Priority: {YELLOW}{state.priority}{RESET} | "
                    f"Status: {state.status}"
                )

    def match_supply(self, crop: str):
        result = self._service.match_supply(crop)
        if not result:
            return None

        oversupply = {
            "lgu": result.oversupply.lgu,
            "crop": result.oversupply.crop,
            "priority": result.oversupply.priority,
        }
        shortage = {
            "lgu": result.shortage.lgu,
            "crop": result.shortage.crop,
            "priority": result.shortage.priority,
        }

        return oversupply, shortage

    @property
    def crops(self) -> dict[str, list[dict[str, object]]]:
        return {
            crop: [
                {"lgu": state.lgu, "crop": state.crop, "priority": state.priority}
                for state in states
            ]
            for crop, states in self._service.list_supply().items()
        }
