# Scenario

Your task is to implement a simplified version of a banking system.
All operations that should be supported are listed below. Partial credit will be granted for each test passed, so
run the tests often to track your progress. Please check the tests for requirements and argument types.

### Implementation Tips

Read the question all the way through before you start coding, but implement the operations and complete the
levels one by one, not all together, keeping in mind that you will need to refactor to support additional functionality.
Please, do not change the existing method signatures.

### Files

- `banking_system.py` – the interface. Do not edit it.
- `banking_system_impl.py` – implement `BankingSystemImpl` here.
- `test_level_<n>.py` – the tests for each level.

Run the tests for a level from this directory:

```bash
python -m unittest test_level_1
```

### Timestamps

Every operation takes a `timestamp` (an `int`, in milliseconds) as its first argument.
Timestamps are unique and strictly increasing across all calls, so operations always arrive in order.

## Level 1 – Initial Design & Basic Functions

The banking system should support creating new accounts, depositing money into accounts, and transferring money
between two accounts. All amounts are positive integers.

- **create_account(timestamp: int, account_id: str) -> bool**
  - Create a new account with the given identifier and a balance of `0`.
  - Return `True` if the account was created.
  - Return `False` if an account with `account_id` already exists.
- **deposit(timestamp: int, account_id: str, amount: int) -> int | None**
  - Deposit `amount` into the account `account_id`.
  - Return the balance of the account after the deposit.
  - Return `None` if the account doesn't exist.
- **transfer(timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None**
  - Move `amount` from `source_account_id` to `target_account_id`.
  - Return the balance of `source_account_id` after the transfer.
  - Return `None` if any of these is true:
    - `source_account_id` or `target_account_id` doesn't exist.
    - `source_account_id` and `target_account_id` are the same.
    - `source_account_id` has less than `amount` in its balance.
  - A failed transfer changes no balances.

## Level 2 – Data Structures & Data Processing

The bank wants to see which accounts move the most money out.

- **top_spenders(timestamp: int, n: int) -> list[str]**
  - Return the identifiers of the top `n` accounts with the highest **outgoing** totals.
  - An account's outgoing total is the sum of all successful transfers sent **from** that account.
    Deposits, incoming transfers and failed transfers don't count.
  - Order by outgoing total, highest first. Break ties by `account_id` in ascending (alphabetical) order.
  - Format each entry as `"<account_id>(<outgoing_total>)"`, for example `["account2(500)", "account1(0)"]`.
  - Accounts with an outgoing total of `0` are included.
  - If there are fewer than `n` accounts, return all of them.

## Level 3 – Refactoring & Encapsulation

The bank now lets customers pay for purchases from their accounts, and every payment earns cashback.
The cashback isn't paid right away: it arrives one day later.

- **pay(timestamp: int, account_id: str, amount: int) -> str | None**
  - Withdraw `amount` from `account_id` as a payment.
  - Return a payment identifier of the form `"payment<k>"`, where `k` counts successful payments across the
    **whole system**, starting at `1`: the first payment is `"payment1"`, the next is `"payment2"`, and so on.
  - Return `None` if the account doesn't exist or its balance is less than `amount`.
    A failed payment changes nothing and doesn't use up a payment number.
  - A payment counts toward the account's outgoing total in `top_spenders`, just like a transfer.
- **Cashback**
  - Each successful payment earns **2%** of `amount` as cashback, **rounded down** to a whole number.
  - The cashback is deposited into the account exactly **24 hours** (`86400000` milliseconds) after the payment:
    a payment at timestamp `t` pays its cashback at `t + 86400000`.
  - Cashback that is due at or before an operation's `timestamp` must be applied **before** that operation runs.
  - Cashback is not outgoing money and doesn't change the outgoing total.
  - A payment whose cashback rounds down to `0` still counts as having received its cashback when it's due.
- **get_payment_status(timestamp: int, account_id: str, payment: str) -> str | None**
  - Return the status of the payment `payment` made from `account_id`:
    - `"IN_PROGRESS"` if its cashback hasn't been deposited yet.
    - `"CASHBACK_RECEIVED"` if its cashback has been deposited.
  - Return `None` if `account_id` doesn't exist, `payment` doesn't exist, or `payment` was made from a different account.
