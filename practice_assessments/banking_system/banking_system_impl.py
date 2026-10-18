from dataclasses import dataclass
from enum import StrEnum
from banking_system import BankingSystem

A_DAY = 86400000


# Done: BankingSystem owns payments and process cashbacks at each operation
# Done: before calculating a balance, apply cashbacks
# Done: same for withdraw and deposit
# Done: In fact, we should apply cashbacks for all accounts on each operation
# Keep paymentid in banking system


class PaymentStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    CASHBACK_RECEIVED = "CASHBACK_RECEIVED"


@dataclass
class Payment:
    id: int
    from_account: str
    amount: int
    timestamp: int
    payout: bool = False

    @property
    def cashback_timestamp(self):
        return self.timestamp + A_DAY

    @property
    def cashback_amount(self):
        return self.amount * 2 // 100

    def status(self, timestamp: int) -> str:
        if timestamp < self.cashback_timestamp:
            return str(PaymentStatus.IN_PROGRESS)
        else:
            return str(PaymentStatus.CASHBACK_RECEIVED)

    def __str__(self) -> str:
        return f"payment{self.id}"


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
        self.payments: list[Payment] = list()

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._process_cashbacks(timestamp)

        if self._exists(account_id):
            return False

        self.accounts[account_id] = Account(account_id, 0)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._process_cashbacks(timestamp)

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
        self._process_cashbacks(timestamp)

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
        self._process_cashbacks(timestamp)

        accounts = sorted(
            self.accounts.values(),
            key=lambda acc: (-acc.total_out(), acc.id),
        )
        return [f"{acc.id}({acc.total_out()})" for acc in accounts[:n]]

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        """
        Withdraw `amount` from `account_id` as a payment that earns 2% cashback
        (rounded down) 24 hours later. Return "payment<k>", or None if the account
        doesn't exist or has too little money.
        """
        if not self._exists(account_id):
            return None

        account = self._get(account_id)
        if account.balance() < amount:
            return None

        payment = Payment(self._next_payment_id(), account.id, amount, timestamp)
        account.withdraw(amount)
        self.payments.append(payment)

        return str(payment)

    def get_payment_status(
        self, timestamp: int, account_id: str, payment: str
    ) -> str | None:
        """
        Return "IN_PROGRESS" or "CASHBACK_RECEIVED" for `payment`, or None if the
        account or payment doesn't exist, or the payment belongs to another account.
        """
        if not self._exists(account_id):
            return None

        payment_id = int(payment[7:])
        payment_obj = self._get_payment(payment_id)

        if payment_obj is None or payment_obj.from_account != account_id:
            return None

        return payment_obj.status(timestamp)

    def _exists(self, account_id: str):
        return account_id in self.accounts

    def _get(self, account_id: str):
        return self.accounts[account_id]

    def _process_cashbacks(self, timestamp: int) -> None:
        for payment in self.payments:
            if not payment.payout and timestamp >= payment.cashback_timestamp:
                self.accounts[payment.from_account].deposit(payment.cashback_amount)
                payment.payout = True

    def _next_payment_id(self) -> int:
        return len(self.payments) + 1

    def _get_payment(self, payment_id: int) -> Payment | None:
        idx = payment_id - 1
        return self.payments[idx] if idx < len(self.payments) else None
