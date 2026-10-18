from dataclasses import dataclass
from banking_system import BankingSystem

A_DAY = 86400000


# Balance must have timestamp
# same for deposit and withdraw
# cashback is now a separate state -> separate object
# an account owns multiple cashbacks
# before calculating a balance, apply cashbacks
# same for withdraw and deposit
# In fact, we should apply cashbacks for all accounts on each operation


@dataclass
class Payment:
    id: str
    amount: int
    timestamp: int

    @property
    def cashback_timestamp(self):
        return self.timestamp + A_DAY


@dataclass
class Account:
    id: str
    _balance: int = 0
    _total_out: int = 0

    def withdraw(self, amount: int) -> int:
        self._balance -= amount
        self._total_out += amount
        return self._balance

    def deposit(self, amount: int) -> int:
        self._balance += amount
        return self._balance

    def balance(self) -> int:
        return self._balance

    def total_out(self) -> int:
        return self._total_out


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.accounts: dict[str, Account] = dict()

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if self._exists(account_id):
            return False

        self.accounts[account_id] = Account(account_id, 0)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if not self._exists(account_id):
            return None

        if amount <= 0:
            raise RuntimeError("Deposit Amount must be more than 0")

        account = self._get(account_id)
        account.deposit(amount)

        return account.balance()

    def transfer(
        self,
        timestamp: int,
        source_account_id: str,
        target_account_id: str,
        amount: int,
    ) -> int | None:
        """
        Move `amount` from `source_account_id` to `target_account_id`.
        Return the source balance after the transfer, or None if either account
        doesn't exist, both are the same account, or the source has too little money.
        """
        if not self._exists(source_account_id) or not self._exists(target_account_id):
            return None

        if source_account_id == target_account_id:
            return None

        source_account = self._get(source_account_id)
        target_account = self._get(target_account_id)

        if source_account.balance() < amount:
            return None

        source_account.withdraw(amount)
        target_account.deposit(amount)

        return source_account.balance()

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Return up to `n` accounts with the highest outgoing totals, formatted as
        "<account_id>(<outgoing_total>)". Highest first, ties by account_id ascending.
        """
        accounts = sorted(
            self.accounts.values(),
            key=lambda acc: (-acc.total_out(), acc.id),
        )
        return [f"{acc.id}({acc.total_out()})" for acc in accounts[:n]]

    def _exists(self, account_id: str):
        return account_id in self.accounts

    def _get(self, account_id: str):
        return self.accounts[account_id]
