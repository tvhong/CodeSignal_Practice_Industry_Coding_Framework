import unittest

from banking_system_impl import BankingSystemImpl

MILLISECONDS_IN_1_DAY = 24 * 60 * 60 * 1000


class Level4Tests(unittest.TestCase):

    def setUp(self):
        self.system = BankingSystemImpl()

    def test_level_4_case_01_merge_accounts(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 500)
        self.system.deposit(4, "account2", 300)
        self.assertTrue(self.system.merge_accounts(5, "account1", "account2"))
        self.assertIsNone(self.system.deposit(6, "account2", 1))
        self.assertEqual(self.system.deposit(7, "account1", 1), 801)
        self.assertIsNone(self.system.transfer(8, "account1", "account2", 1))

    def test_level_4_case_02_merge_failures(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 100)
        self.system.deposit(4, "account2", 200)
        self.assertFalse(self.system.merge_accounts(5, "account1", "account1"))
        self.assertFalse(self.system.merge_accounts(6, "account1", "account3"))
        self.assertFalse(self.system.merge_accounts(7, "account3", "account1"))
        self.assertEqual(self.system.deposit(8, "account1", 1), 101)
        self.assertEqual(self.system.deposit(9, "account2", 1), 201)
        self.assertTrue(self.system.merge_accounts(10, "account2", "account1"))
        self.assertEqual(self.system.deposit(11, "account2", 1), 303)

    def test_level_4_case_03_merge_combines_outgoing(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.create_account(3, "account3")
        self.system.deposit(4, "account1", 1000)
        self.system.deposit(5, "account2", 1000)
        self.system.transfer(6, "account1", "account3", 300)
        self.system.transfer(7, "account2", "account3", 200)
        self.assertEqual(self.system.pay(8, "account2", 100), "payment1")
        self.assertEqual(
            self.system.top_spenders(9, 3),
            ["account1(300)", "account2(300)", "account3(0)"],
        )
        self.assertTrue(self.system.merge_accounts(10, "account1", "account2"))
        self.assertEqual(self.system.top_spenders(11, 3), ["account1(600)", "account3(0)"])

    def test_level_4_case_04_merge_moves_pending_cashback(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account2", 1000)
        self.assertEqual(self.system.pay(4, "account2", 500), "payment1")
        self.assertTrue(self.system.merge_accounts(5, "account1", "account2"))
        self.assertEqual(self.system.get_payment_status(6, "account1", "payment1"), "IN_PROGRESS")
        self.assertIsNone(self.system.get_payment_status(7, "account2", "payment1"))
        self.assertEqual(
            self.system.get_payment_status(4 + MILLISECONDS_IN_1_DAY, "account1", "payment1"),
            "CASHBACK_RECEIVED",
        )
        self.assertEqual(self.system.deposit(5 + MILLISECONDS_IN_1_DAY, "account1", 1), 511)

    def test_level_4_case_05_recreate_merged_account(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 100)
        self.system.deposit(4, "account2", 50)
        self.assertEqual(self.system.pay(5, "account2", 50), "payment1")
        self.assertTrue(self.system.merge_accounts(6, "account1", "account2"))
        self.assertTrue(self.system.create_account(7, "account2"))
        self.assertEqual(self.system.deposit(8, "account2", 20), 20)
        self.assertIsNone(self.system.get_payment_status(9, "account2", "payment1"))
        self.assertEqual(self.system.get_payment_status(10, "account1", "payment1"), "IN_PROGRESS")
        self.assertEqual(self.system.top_spenders(11, 2), ["account1(50)", "account2(0)"])

    def test_level_4_case_06_get_balance(self):
        self.system.create_account(10, "account1")
        self.system.deposit(20, "account1", 100)
        self.system.deposit(30, "account1", 50)
        self.assertIsNone(self.system.get_balance(40, "account1", 5))
        self.assertEqual(self.system.get_balance(41, "account1", 10), 0)
        self.assertEqual(self.system.get_balance(42, "account1", 20), 100)
        self.assertEqual(self.system.get_balance(43, "account1", 25), 100)
        self.assertEqual(self.system.get_balance(44, "account1", 30), 150)
        self.assertEqual(self.system.get_balance(45, "account1", 45), 150)
        self.assertIsNone(self.system.get_balance(46, "account2", 30))

    def test_level_4_case_07_get_balance_after_transfers_and_payments(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.system.transfer(4, "account1", "account2", 400)
        self.assertEqual(self.system.pay(5, "account2", 100), "payment1")
        self.assertEqual(self.system.get_balance(6, "account1", 4), 600)
        self.assertEqual(self.system.get_balance(7, "account2", 3), 0)
        self.assertEqual(self.system.get_balance(8, "account2", 4), 400)
        self.assertEqual(self.system.get_balance(9, "account2", 5), 300)
        self.assertEqual(self.system.get_balance(10, "account1", 3), 1000)

    def test_level_4_case_08_get_balance_includes_cashback_at_due_time(self):
        self.system.create_account(1, "account1")
        self.system.deposit(2, "account1", 1000)
        self.assertEqual(self.system.pay(10, "account1", 500), "payment1")
        self.assertEqual(
            self.system.get_balance(20 + MILLISECONDS_IN_1_DAY, "account1", 10 + MILLISECONDS_IN_1_DAY - 1),
            500,
        )
        self.assertEqual(
            self.system.get_balance(21 + MILLISECONDS_IN_1_DAY, "account1", 10 + MILLISECONDS_IN_1_DAY),
            510,
        )
        self.assertEqual(self.system.get_balance(22 + MILLISECONDS_IN_1_DAY, "account1", 10), 500)

    def test_level_4_case_09_get_balance_across_merge_and_recreate(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 100)
        self.system.deposit(4, "account2", 200)
        self.assertTrue(self.system.merge_accounts(10, "account1", "account2"))
        self.assertTrue(self.system.create_account(20, "account2"))
        self.system.deposit(30, "account2", 5)
        self.assertEqual(self.system.get_balance(40, "account1", 9), 100)
        self.assertEqual(self.system.get_balance(41, "account1", 10), 300)
        self.assertEqual(self.system.get_balance(42, "account2", 9), 200)
        self.assertIsNone(self.system.get_balance(43, "account2", 10))
        self.assertIsNone(self.system.get_balance(44, "account2", 15))
        self.assertEqual(self.system.get_balance(45, "account2", 20), 0)
        self.assertEqual(self.system.get_balance(46, "account2", 30), 5)

    def test_level_4_case_10_get_balance_with_cashback_after_merge(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account2", 1000)
        self.assertEqual(self.system.pay(4, "account2", 1000), "payment1")
        self.assertTrue(self.system.merge_accounts(5, "account1", "account2"))
        self.assertEqual(
            self.system.get_balance(10 + MILLISECONDS_IN_1_DAY, "account1", 4 + MILLISECONDS_IN_1_DAY),
            20,
        )
        self.assertEqual(self.system.get_balance(11 + MILLISECONDS_IN_1_DAY, "account1", 5), 0)
        self.assertEqual(self.system.get_balance(12 + MILLISECONDS_IN_1_DAY, "account2", 4), 0)
        self.assertEqual(self.system.get_balance(13 + MILLISECONDS_IN_1_DAY, "account2", 3), 1000)


if __name__ == "__main__":
    unittest.main()
