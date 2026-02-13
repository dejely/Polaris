from __future__ import annotations

import argparse
from typing import Sequence

from agriPolaris.application.service import SupplyMonitorService
from agriPolaris.infrastructure.sqlite_repository import SQLiteSupplyRepository

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="POLARIS: Agricultural Logistics Monitoring")
    parser.add_argument("--add", action="store_true", help="Add or update an LGU supply entry")
    parser.add_argument("--cget", action="store_true", help="Get most critical LGU")
    parser.add_argument("--list", action="store_true", help="List all crop queues and records")
    parser.add_argument(
        "--flush",
        choices=["true", "false"],
        help="Flush all supply records from storage",
    )
    parser.add_argument("--match", action="store_true", help="Match oversupply to shortage for a crop")

    parser.add_argument("--lgu", type=str, help="LGU name")
    parser.add_argument("--crop", type=str, help="Crop type")
    parser.add_argument("--curr", type=int, help="Current supply")
    parser.add_argument("--ideal", type=int, help="Ideal supply")
    parser.add_argument("--db", type=str, default="entries.db", help="SQLite database path")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    service = SupplyMonitorService(SQLiteSupplyRepository(db_path=args.db))

    if args.add:
        if not (args.lgu and args.crop and args.curr is not None and args.ideal is not None):
            parser.error("--add requires --lgu, --crop, --curr, and --ideal")

        state = service.upsert_supply(
            lgu=args.lgu,
            crop=args.crop,
            current_supply=args.curr,
            ideal_supply=args.ideal,
        )
        print(
            f"Added {BOLD}{state.lgu}{RESET} for {BOLD}{state.crop}{RESET} "
            f"with priority {YELLOW}{state.priority}{RESET}."
        )

    if args.match:
        if not args.crop:
            parser.error("--match requires --crop")

        matched = service.match_supply(args.crop)
        if not matched:
            print(f"No valid oversupply/shortage match available for {args.crop!r}.")
            return 0

        print(f"--- MATCH RESULTS FOR {matched.oversupply.crop} ---")
        print(
            f"Oversupply: {GREEN}{BOLD}{matched.oversupply.lgu}{RESET} "
            f"({YELLOW}{matched.oversupply.priority}{RESET})"
        )
        print(
            f"Shortage: {RED}{BOLD}{matched.shortage.lgu}{RESET} "
            f"({YELLOW}{matched.shortage.priority}{RESET})"
        )
        print("\nRecommendation:")
        print(
            f"Transfer {matched.oversupply.crop} from {GREEN}{matched.oversupply.lgu}{RESET} "
            f"-> {RED}{matched.shortage.lgu}{RESET}"
        )

    if args.list:
        all_supply = service.list_supply()
        if not all_supply:
            print("No records found.")
        for crop, states in all_supply.items():
            print(f"\nCrop: {YELLOW}{crop}{RESET}")
            if not states:
                print("  (empty)")
                continue
            for state in states:
                print(
                    f"  LGU: {BOLD}{state.lgu}{RESET} "
                    f"| Priority: {YELLOW}{state.priority}{RESET} "
                    f"| Status: {state.status}"
                )

    if args.cget:
        critical = service.get_most_critical(args.crop) if args.crop else service.get_most_critical()
        if not critical:
            print("No critical LGU found. Add entries first.")
        else:
            print(
                f"Most critical LGU: {BOLD}{critical.lgu}{RESET} "
                f"({critical.crop}, priority={critical.priority})"
            )

    if args.flush == "true":
        service.flush()
        print("Database flushed.")

    if not any([args.add, args.match, args.list, args.cget, args.flush]):
        parser.print_help()

    return 0


def main() -> None:
    raise SystemExit(run())
