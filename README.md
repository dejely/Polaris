# 🌟Polaris
**_A Structured Redistribution Engine for Crop Supply Monitoring and Agricultural Logistics_**
## 📖 Overview
POLARIS is an agricultural logistics system built to monitor the supply conditions of various crops across Local Government Units (LGUs).

It uses:
- **Signed priority values** (key > 0 = Oversupply | key < 0 = Undersupply)
- **Per-crop database tables** in SQLite!
- **Per-Crop Priority Queues** implemented using a DLL!
- **2D Priority Structure** Grouping PQs by crop type!
- **CLI control interface** for adding, listing, and evaluating LGU Supply States!
  
POLARIS aims to support logistics balancing:

matching **oversupplied regions** with **undersupplied regions** efficiently for sustainable food distribution.

## 🚀 Key Features
🔹 **Signed Priority System**

POLARIS computes supply difference as:
```ruby
priority = curr_supply - ideal_supply
```
- Positive priority -> Oversupply
- Negative priority -> Undersupply
- Zero → Perfectly balanced supply

The Priority Queue System is max-based, so the largest shortage (most negative) gets paired up with the **highest** priority.

🔹 Per-Crop Architecture (Dynamic Tables)

Each crop automatically creates its own table inside the SQLite database:
```ruby
rice(_lgu TEXT UNIQUE, key INTEGER)
corn(_lgu TEXT UNIQUE, key INTEGER)
onion(_lgu TEXT UNIQUE, key INTEGER)
...
```

This avoids cross-crop contamination and keeps the database clean and scalable.

🔹 2D Priority Queue Structure

POLARIS maintains:
```makefile
"Rice": PQ_of_Rice
"Corn": PQ_of_Corn
"Onion": PQ_of_Onion
...
```
This acts like a _2D priority system_, where each crop has its own queue sorted by imbalance severity.
🔹 Automatic Oversupply → Undersupply Matching

Because priorities are signed:
- Most positive = largest oversupply
- Most negative = largest undersupply
```ruby
PQ[crop][0]   → LGU with worst shortage
PQ[crop][-1]  → LGU with worst oversupply
```
This enables logistics pairing:
```makefile
Send oversupply → to undersupply region
```
🔹 SQLite Integration

Data persists through:

- Crop-specific tables
- UPSERT behavior (INSERT OR REPLACE)
- Full or soft database flushing

## Command Line Interface
Use POLARIS through simple commands:
| Command | Description |
|:-----------|:-------------|
| --add          | Add or update LGU crop supply             | 
| --list          | Show all PQs and DB tables             | 
| --cget          | Retrieve the most critical imbalance               |
| --flush=true           | Clear all crop tables               |

## 🧮 Priority Calculation
Given: 
```ruby
curr_supply
ideal_supply
```
Priority = signed difference:
```ruby
priority = curr_supply - ideal_supply
```
Examples:
| Curr | Ideal | Difference(key) | Meaning    |
|:-----------|:-------------:|------------:|------------:|
| 500          | 300             | +200           | Oversupply             |
| 100          | 300             | -200           | Undersupply            |
| 200          | 200             | 0              | Balanced              |

### PQ Priority:
- Largest positive -> biggest oversupply -> biggest priority
- Most negative -> biggest shortage -> lowest priority (unless changed)
