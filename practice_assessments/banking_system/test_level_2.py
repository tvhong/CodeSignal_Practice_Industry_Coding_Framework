import unittest

from banking_system_impl import BankingSystemImpl


class Level2Tests(unittest.TestCase):

    def setUp(self):
        self.system = BankingSystemImpl()

    def test_level_2_case_01_orders_by_outgoing(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.create_account(3, "account3")
        self.system.deposit(4, "account1", 1000)
        self.system.deposit(5, "account2", 1000)
        self.system.deposit(6, "account3", 1000)
        self.system.transfer(7, "account1", "account2", 100)
        self.system.transfer(8, "account2", "account3", 400)
        self.system.transfer(9, "account3", "account1", 250)
        self.assertEqual(
            self.system.top_spenders(10, 3),
            ["account2(400)", "account3(250)", "account1(100)"],
        )

    def test_level_2_case_02_ties_sorted_by_account_id(self):
        self.system.create_account(1, "bob")
        self.system.create_account(2, "alice")
        self.system.create_account(3, "carol")
        self.system.deposit(4, "bob", 500)
        self.system.deposit(5, "alice", 500)
        self.system.transfer(6, "bob", "carol", 200)
        self.system.transfer(7, "alice", "carol", 200)
        self.assertEqual(
            self.system.top_spenders(8, 3),
            ["alice(200)", "bob(200)", "carol(0)"],
        )

    def test_level_2_case_03_n_smaller_than_account_count(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.create_account(3, "account3")
        self.system.deposit(4, "account3", 900)
        self.system.transfer(5, "account3", "account1", 300)
        self.system.transfer(6, "account1", "account2", 50)
        self.assertEqual(self.system.top_spenders(7, 1), ["account3(300)"])
        self.assertEqual(self.system.top_spenders(8, 2), ["account3(300)", "account1(50)"])

    def test_level_2_case_04_n_larger_than_account_count(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.assertEqual(self.system.top_spenders(3, 5), ["account1(0)", "account2(0)"])

    def test_level_2_case_05_outgoing_accumulates(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.system.transfer(4, "account1", "account2", 100)
        self.system.transfer(5, "account1", "account2", 200)
        self.system.transfer(6, "account2", "account1", 300)
        self.system.transfer(7, "account1", "account2", 50)
        self.assertEqual(
            self.system.top_spenders(8, 2),
            ["account1(350)", "account2(300)"],
        )

    def test_level_2_case_06_deposits_and_failed_transfers_do_not_count(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 5000)
        self.system.deposit(4, "account2", 100)
        self.assertIsNone(self.system.transfer(5, "account2", "account1", 101))
        self.assertIsNone(self.system.transfer(6, "account1", "account3", 10))
        self.assertIsNone(self.system.transfer(7, "account1", "account1", 10))
        self.assertEqual(self.system.transfer(8, "account2", "account1", 1), 99)
        self.assertEqual(
            self.system.top_spenders(9, 2),
            ["account2(1)", "account1(0)"],
        )

    def test_level_2_case_07_ranking_changes_over_time(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 1000)
        self.system.deposit(4, "account2", 1000)
        self.system.transfer(5, "account1", "account2", 300)
        self.assertEqual(self.system.top_spenders(6, 2), ["account1(300)", "account2(0)"])
        self.system.transfer(7, "account2", "account1", 500)
        self.assertEqual(self.system.top_spenders(8, 2), ["account2(500)", "account1(300)"])


if __name__ == "__main__":
    unittest.main()
