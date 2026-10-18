# Scenario

Your task is to implement a simplified version of an in-memory database.
All operations that should be supported are listed below. Partial credit will be granted for each test passed, so
run the tests often to track your progress. Please check the tests for requirements and argument types.

### Implementation Tips

Read the question all the way through before you start coding, but implement the operations and complete the
levels one by one, not all together, keeping in mind that you will need to refactor to support additional functionality.
Please, do not change the existing method signatures.

### Files

- `in_memory_db.py` – the interface. Do not edit it.
- `in_memory_db_impl.py` – implement `InMemoryDBImpl` here.
- `test_level_<n>.py` – the tests for each level.

Run the tests for a level from this directory:

```bash
python -m unittest test_level_1
```

### Records

The database stores **records**. Each record is identified by a `key` and holds any number of **fields**,
and each field has a string `value`. For example, the record `"user1"` might hold the fields
`"name" → "Ada"` and `"city" → "London"`.

Keys, fields and values are non-empty strings.

## Level 1 – Initial Design & Basic Functions

The database should support setting, reading and deleting a field within a record.

- **set(key: str, field: str, value: str) -> None**
  - Set `field` in the record `key` to `value`.
  - If the record doesn't exist, create it.
  - If the field already exists, replace its value.
- **get(key: str, field: str) -> str | None**
  - Return the value of `field` in the record `key`.
  - Return `None` if the record or the field doesn't exist.
- **delete(key: str, field: str) -> bool**
  - Remove `field` from the record `key`.
  - Return `True` if the field existed and was removed.
  - Return `False` if the record or the field doesn't exist.
  - A record with no fields left is treated as if it doesn't exist.

## Level 2 – Data Structures & Data Processing

The database should support listing the fields of a record.

- **scan(key: str) -> list[str]**
  - Return every field of the record `key`, formatted as `"<field>(<value>)"`,
    for example `["city(London)", "name(Ada)"]`.
  - Order by field name in ascending order, comparing names as plain strings character by character:
    uppercase letters come before lowercase ones, and `"a10"` comes before `"a2"`.
  - Return an empty list if the record doesn't exist.
- **scan_by_prefix(key: str, prefix: str) -> list[str]**
  - Same as `scan`, but only include fields whose name starts with `prefix`.
  - The match is case-sensitive.
  - Return an empty list if the record doesn't exist or no field matches.

## Level 3 – Refactoring & Encapsulation

The database now needs to support fields that expire. Every operation in this level takes a `timestamp`
(an `int`, in milliseconds) as its first argument, and fields can be given a **time to live** (TTL).

Add a timestamped version of every Level 1 and Level 2 operation. Each one behaves exactly like the
original, except as described below. Keep the Level 1 and Level 2 methods working as before.

- Timestamps are unique and strictly increasing across all calls, so operations always arrive in order.
- Tests for this level and later only call the timestamped methods. You never need to handle a mix of
  timestamped and non-timestamped calls on the same database.

### TTL

- A field set with a TTL of `ttl` at timestamp `t` is **visible** from `t` up to, but **not including**, `t + ttl`.
  At `t + ttl` and after, it has **expired**.
- An expired field is treated as if it doesn't exist: `get_at` doesn't return it, `delete_at` returns `False`,
  and scans don't list it. A record whose fields have all expired is treated as if it doesn't exist.
- `ttl` is a positive integer.

### Operations

- **set_at(timestamp: int, key: str, field: str, value: str) -> None**
  - Like `set`. The field never expires.
  - If the field already had a TTL, the TTL is removed: the new value never expires.
- **set_at_with_ttl(timestamp: int, key: str, field: str, value: str, ttl: int) -> None**
  - Like `set_at`, but the field expires at `timestamp + ttl`.
  - If the field already existed, both its value and its expiry are replaced.
- **delete_at(timestamp: int, key: str, field: str) -> bool**
  - Like `delete`. Return `False` if the field has expired.
- **get_at(timestamp: int, key: str, field: str) -> str | None**
  - Like `get`. Return `None` if the field has expired.
- **scan_at(timestamp: int, key: str) -> list[str]**
  - Like `scan`, but only fields that are visible at `timestamp`.
- **scan_by_prefix_at(timestamp: int, key: str, prefix: str) -> list[str]**
  - Like `scan_by_prefix`, but only fields that are visible at `timestamp`.

## Level 4 – Extending Design & Functionality

The database should support saving its state and rolling back to an earlier save.

- **backup(timestamp: int) -> int**
  - Save a copy of the whole database as it is at `timestamp`.
  - Return the number of records that have at least one field visible at `timestamp`.
  - Only visible fields are saved. A field that has expired at `timestamp` is not part of the backup.
  - For each saved field with a TTL, the backup stores its **remaining** TTL: its expiry time minus `timestamp`.
  - Later changes to the database don't change a backup that has already been made.
- **restore(timestamp: int, timestamp_to_restore: int) -> None**
  - Replace the whole database with the **latest** backup taken at or before `timestamp_to_restore`.
    Everything in the database that isn't in that backup is gone.
  - `timestamp_to_restore` is always earlier than `timestamp`, and at least one backup exists at or before it.
  - Each restored field with a TTL gets a new expiry time: `timestamp` plus the remaining TTL saved in the backup.
    For example, a field backed up with 7 ms left and restored at `20` expires at `27`.
  - Fields that had no TTL still have no TTL.
  - Restoring doesn't remove any backups. Later calls can restore from any backup again, including
    the same one, and later changes don't affect the backups.
