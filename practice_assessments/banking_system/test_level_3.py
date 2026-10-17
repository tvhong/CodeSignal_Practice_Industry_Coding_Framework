import unittest

from banking_system_impl import BankingSystemImpl

MILLISECONDS_IN_1_DAY = 24 * 60 * 60 * 1000


class Level3Tests(unittest.TestCase):

    def setUp(self):
        self.system = BankingSystemImpl()

    def test_level_3_case_01_pay(self):
        self.system.create_account(1, "account1")
        self.system.deposit(2, "account1", 1000)
        self.assertEqual(self.system.pay(3, "account1", 300), "payment1")
        self.assertEqual(self.system.deposit(4, "account1", 1), 701)
        self.assertEqual(self.system.pay(5, "account1", 100), "payment2")
        self.assertEqual(self.system.deposit(6, "account1", 1), 602)

    def test_level_3_case_02_pay_failures(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 100)
        self.assertIsNone(self.system.pay(4, "account3", 10))
        self.assertIsNone(self.system.pay(5, "account1", 101))
        self.assertIsNone(self.system.pay(6, "account2", 1))
        self.assertEqual(self.system.pay(7, "account1", 100), "payment1")
        self.assertEqual(self.system.deposit(8, "account1", 1), 1)

    def test_level_3_case_03_payment_numbers_are_global(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.system.deposit(4, "account2", 1000)
        self.assertEqual(self.system.pay(5, "account1", 10), "payment1")
        self.assertEqual(self.system.pay(6, "account2", 10), "payment2")
        self.assertEqual(self.system.pay(7, "account1", 10), "payment3")

    def test_level_3_case_04_cashback_arrives_after_24_hours(self):
        self.system.create_account(1, "account1")
        self.system.deposit(2, "account1", 1000)
        self.assertEqual(self.system.pay(10, "account1", 500), "payment1")
        self.assertEqual(self.system.deposit(10 + MILLISECONDS_IN_1_DAY - 1, "account1", 1), 501)
        self.assertEqual(self.system.deposit(10 + MILLISECONDS_IN_1_DAY, "account1", 1), 512)

    def test_level_3_case_05_cashback_rounds_down(self):
        self.system.create_account(1, "account1")
        self.system.deposit(2, "account1", 1000)
        self.assertEqual(self.system.pay(3, "account1", 149), "payment1")
        self.assertEqual(self.system.pay(4, "account1", 49), "payment2")
        self.assertEqual(self.system.deposit(4 + MILLISECONDS_IN_1_DAY, "account1", 1), 805)
        self.assertEqual(
            self.system.get_payment_status(5 + MILLISECONDS_IN_1_DAY, "account1", "payment2"),
            "CASHBACK_RECEIVED",
        )

    def test_level_3_case_06_payment_status(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.assertEqual(self.system.pay(4, "account1", 200), "payment1")
        self.assertEqual(self.system.get_payment_status(5, "account1", "payment1"), "IN_PROGRESS")
        self.assertIsNone(self.system.get_payment_status(6, "account2", "payment1"))
        self.assertIsNone(self.system.get_payment_status(7, "account1", "payment2"))
        self.assertIsNone(self.system.get_payment_status(8, "account3", "payment1"))
        self.assertEqual(
            self.system.get_payment_status(4 + MILLISECONDS_IN_1_DAY - 1, "account1", "payment1"),
            "IN_PROGRESS",
        )
        self.assertEqual(
            self.system.get_payment_status(4 + MILLISECONDS_IN_1_DAY, "account1", "payment1"),
            "CASHBACK_RECEIVED",
        )

    def test_level_3_case_07_payments_count_as_outgoing(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.system.deposit(4, "account2", 1000)
        self.system.pay(5, "account1", 300)
        self.system.transfer(6, "account2", "account1", 200)
        self.system.pay(7, "account2", 50)
        self.assertEqual(self.system.top_spenders(8, 2), ["account1(300)", "account2(250)"])
        self.assertEqual(
            self.system.top_spenders(8 + MILLISECONDS_IN_1_DAY, 2),
            ["account1(300)", "account2(250)"],
        )

    def test_level_3_case_08_cashback_applied_before_operation(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.assertEqual(self.system.pay(4, "account1", 1000), "payment1")
        self.assertIsNone(self.system.transfer(5, "account1", "account2", 20))
        self.assertEqual(self.system.transfer(4 + MILLISECONDS_IN_1_DAY, "account1", "account2", 20), 0)

    def test_level_3_case_09_multiple_cashbacks(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 10000)
        self.system.deposit(4, "account2", 5000)
        self.assertEqual(self.system.pay(100, "account1", 1000), "payment1")
        self.assertEqual(self.system.pay(200, "account2", 2000), "payment2")
        self.assertEqual(self.system.pay(300, "account1", 500), "payment3")
        self.assertEqual(
            self.system.get_payment_status(200 + MILLISECONDS_IN_1_DAY, "account2", "payment2"),
            "CASHBACK_RECEIVED",
        )
        self.assertEqual(
            self.system.get_payment_status(201 + MILLISECONDS_IN_1_DAY, "account1", "payment1"),
            "CASHBACK_RECEIVED",
        )
        self.assertEqual(
            self.system.get_payment_status(202 + MILLISECONDS_IN_1_DAY, "account1", "payment3"),
            "IN_PROGRESS",
        )
        self.assertEqual(self.system.deposit(300 + MILLISECONDS_IN_1_DAY, "account1", 1), 8531)
        self.assertEqual(self.system.deposit(301 + MILLISECONDS_IN_1_DAY, "account2", 1), 3041)


if __name__ == "__main__":
    unittest.main()
