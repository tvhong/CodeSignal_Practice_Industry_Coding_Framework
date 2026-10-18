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
