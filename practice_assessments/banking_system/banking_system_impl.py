from dataclasses import dataclass
from banking_system import BankingSystem


@dataclass
class Account:
    id: str
    balance: int


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
        account.balance += amount

        return account.balance

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

        if source_account.balance < amount:
            return None

        source_account.balance -= amount
        target_account.balance += amount

        return source_account.balance

    def _exists(self, account_id: str):
        return account_id in self.accounts

    def _get(self, account_id: str):
        return self.accounts[account_id]
