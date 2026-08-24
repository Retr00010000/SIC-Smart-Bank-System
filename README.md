# SIC Smart Bank System

A Python-based banking and account management CLI application demonstrating core data structure manipulation, multi-currency wallet transactions, role-based reporting with Python set algebra, 2D matrix branch simulation, and persistent JSON storage.

---

## Features

### 1. Authentication & Role Management
* **Dynamic ID Generation:** Auto-assigns incremental unique user IDs.
* **Brute-force Protection:** Limits failed authentication attempts to 3 consecutive tries.
* **Role Separation:** Distinct permissions and view logic for Standard, VIP, and Admin accounts.

### 2. Multi-Currency Wallet & Slicing
* **Real-time Conversion:** Handles multi-currency deposits and withdrawals (`EGP`, `USD`, `SAR`) normalized to standard base balances.
* **Account Transfers:** Secure peer-to-peer balance transfers with real-time sender/receiver verification.
* **History Slicing:** Inspect transaction logs by first operation (`[0]`), last operation (`[-1]`), or recent activity slice (`[-5:]`).

### 3. ATM Network Simulator (2D Matrix)
* **Matrix Grid:** Simulates branch ATM terminals via a 2D list with support for jagged column rendering.
* **Status Monitoring:** Real-time calculation of available vs. out-of-service terminals.
* **Admin Overrides:** Direct terminal state modification using coordinate indexing (`[row][col]`).

### 4. Safe Snapshot & Dictionary Management
* **Defensive Snapshots:** Leverages `copy.deepcopy()` to create isolated state backups prior to user profile modifications.
* **Dynamic Custom Fields:** Allows adding and popping optional metadata fields without mutating core schema constraints.
* **State Rollback:** Restores lost or overwritten fields directly from cached snapshots.

### 5. Analytics & Set Operations (Admin)
* **Set Theory Analysis:** Segment overlap computation utilizing Python bitwise set operations (`&`, `|`, `-`, `^`) across Active, VIP, Failed Login, and Transfer cohorts.
* **Duplicate Detection:** Automatic collision detection for emails and phone numbers across all records.
* **Transaction Aggregation:** Category-wide frequency counting via `dict.fromkeys()` structures.
