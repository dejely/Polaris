# Polaris

Structured crop supply monitoring and redistribution planning.

## Overview
Polaris tracks per-LGU supply imbalances for crops and helps identify transfer opportunities from oversupply areas to shortage areas.

Priority is computed as:

```text
priority = current_supply - ideal_supply
```

- `priority > 0`: oversupply
- `priority < 0`: shortage
- `priority = 0`: balanced

## Scalable Architecture
The repository has been refactored to a layered architecture:

```text
src/agriPolaris/
  application/     # use-case orchestration and service layer
  cli/             # command-line entrypoints
  domain/          # core models, validation, and priority indexing
  infrastructure/  # SQLite persistence and schema/migration logic
  legacy/          # old data structures kept for compatibility
  modules/         # compatibility re-exports for previous imports
  supply_monitor.py# backward-compatible facade
```

## Installation

```bash
pip install -e .
```

## CLI Usage

Use module entrypoint:

```bash
python -m agriPolaris.main --help
```

or installed script:

```bash
agripolaris --help
```

### Add or update a record

```bash
agripolaris --add --lgu "Your LGU" --crop "Rice" --curr 500 --ideal 300
```

### List records

```bash
agripolaris --list
```

### Match oversupply to shortage

```bash
agripolaris --match --crop "Rice"
```

### Get most critical LGU

```bash
agripolaris --cget
```

### Flush records

```bash
agripolaris --flush true
```

## Programmatic Usage

```python
from agriPolaris.application.service import SupplyMonitorService
from agriPolaris.infrastructure.sqlite_repository import SQLiteSupplyRepository

service = SupplyMonitorService(SQLiteSupplyRepository("entries.db"))
service.upsert_supply(lgu="City A", crop="Rice", current_supply=500, ideal_supply=300)
```