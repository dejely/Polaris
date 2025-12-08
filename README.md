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
```
priority = curr_supply - ideal_supply
```
- Positive priority -> Oversupply
- Negative priority -> Undersupply
- Zero → Perfectly balanced supply

The Priority Queue System is max-based, so the largest shortage (most negative) gets paired up with the **highest** priority.
