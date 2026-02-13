from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from agriPolaris.application.service import SupplyMonitorService
from agriPolaris.infrastructure.sqlite_repository import SQLiteSupplyRepository


class SupplyMonitorServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "entries.db"
        self.service = SupplyMonitorService(SQLiteSupplyRepository(str(self.db_path)))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_upsert_and_list_supply(self) -> None:
        self.service.upsert_supply(lgu="LGU-A", crop="Rice", current_supply=500, ideal_supply=300)
        self.service.upsert_supply(lgu="LGU-B", crop="Rice", current_supply=120, ideal_supply=300)

        supply = self.service.list_supply()
        self.assertIn("Rice", supply)
        self.assertEqual(len(supply["Rice"]), 2)
        self.assertEqual(supply["Rice"][0].lgu, "LGU-B")
        self.assertEqual(supply["Rice"][0].priority, -180)
        self.assertEqual(supply["Rice"][1].lgu, "LGU-A")
        self.assertEqual(supply["Rice"][1].priority, 200)

    def test_match_supply_requires_shortage_and_oversupply(self) -> None:
        self.service.upsert_supply(lgu="LGU-A", crop="Rice", current_supply=500, ideal_supply=300)
        self.service.upsert_supply(lgu="LGU-B", crop="Rice", current_supply=120, ideal_supply=300)

        matched = self.service.match_supply("Rice")
        self.assertIsNotNone(matched)
        self.assertEqual(matched.oversupply.lgu, "LGU-A")
        self.assertEqual(matched.shortage.lgu, "LGU-B")

    def test_flush_clears_records(self) -> None:
        self.service.upsert_supply(lgu="LGU-A", crop="Rice", current_supply=500, ideal_supply=300)
        self.service.flush()

        self.assertEqual(self.service.list_supply(), {})

    def test_migrates_legacy_crop_tables(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE rice (_lgu TEXT UNIQUE, key INTEGER)")
            cursor.execute("INSERT INTO rice (_lgu, key) VALUES (?, ?)", ("LGU-LEGACY", -250))
            connection.commit()

        migrated_service = SupplyMonitorService(SQLiteSupplyRepository(str(self.db_path)))
        supply = migrated_service.list_supply()
        self.assertIn("Rice", supply)
        self.assertEqual(supply["Rice"][0].lgu, "LGU-LEGACY")
        self.assertEqual(supply["Rice"][0].priority, 250)


if __name__ == "__main__":
    unittest.main()
