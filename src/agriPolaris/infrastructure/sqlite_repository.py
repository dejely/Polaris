from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from agriPolaris.application.repository import RepositoryRecord
from agriPolaris.domain.validation import normalize_crop, normalize_lgu

_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class SQLiteSupplyRepository:
    def __init__(self, db_path: str = "entries.db") -> None:
        self._db_path = Path(db_path)

    def initialize(self) -> None:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS supply_entries (
                    crop TEXT NOT NULL,
                    lgu TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (crop, lgu)
                )
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_supply_entries_crop_priority
                ON supply_entries (crop, priority)
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_supply_entries_lgu
                ON supply_entries (lgu)
                """
            )

            self._migrate_legacy_tables(cursor)
            connection.commit()

    def upsert(self, *, crop: str, lgu: str, priority: int) -> None:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO supply_entries (crop, lgu, priority)
                VALUES (?, ?, ?)
                ON CONFLICT(crop, lgu)
                DO UPDATE SET
                    priority = excluded.priority,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (crop, lgu, priority),
            )
            connection.commit()

    def fetch_all(self) -> list[RepositoryRecord]:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT crop, lgu, priority
                FROM supply_entries
                ORDER BY crop ASC, priority ASC, lgu ASC
                """
            )
            return [
                RepositoryRecord(crop=row[0], lgu=row[1], priority=int(row[2]))
                for row in cursor.fetchall()
            ]

    def clear(self) -> None:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM supply_entries")

            for table_name in self._list_legacy_tables(cursor):
                cursor.execute(f"DELETE FROM {self._quote_identifier(table_name)}")

            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _migrate_legacy_tables(self, cursor: sqlite3.Cursor) -> None:
        for table_name in self._list_legacy_tables(cursor):
            cursor.execute(f"SELECT _lgu, key FROM {self._quote_identifier(table_name)}")
            rows = cursor.fetchall()

            for lgu, key in rows:
                if lgu is None:
                    continue

                try:
                    normalized_crop = normalize_crop(table_name)
                    normalized_lgu = normalize_lgu(str(lgu))
                except ValueError:
                    continue

                priority = -int(key)
                cursor.execute(
                    """
                    INSERT INTO supply_entries (crop, lgu, priority)
                    VALUES (?, ?, ?)
                    ON CONFLICT(crop, lgu)
                    DO UPDATE SET
                        priority = excluded.priority,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (normalized_crop, normalized_lgu, priority),
                )

    def _list_legacy_tables(self, cursor: sqlite3.Cursor) -> list[str]:
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                AND name != 'supply_entries'
            """
        )

        table_names: list[str] = []
        for row in cursor.fetchall():
            table_name = str(row[0])
            if not _IDENTIFIER_PATTERN.fullmatch(table_name):
                continue

            cursor.execute(f"PRAGMA table_info({self._quote_identifier(table_name)})")
            columns = {str(column[1]) for column in cursor.fetchall()}
            if {"_lgu", "key"}.issubset(columns):
                table_names.append(table_name)

        return table_names

    @staticmethod
    def _quote_identifier(name: str) -> str:
        if not _IDENTIFIER_PATTERN.fullmatch(name):
            raise ValueError(f"Unsafe identifier: {name}")
        return f'"{name}"'
