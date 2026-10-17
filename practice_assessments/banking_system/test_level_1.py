import unittest

from banking_system_impl import BankingSystemImpl


class Level1Tests(unittest.TestCase):

    def setUp(self):
        self.system = BankingSystemImpl()

    def test_level_1_case_01_create_account(self):
        self.assertTrue(self.system.create_account(1, "account1"))
        self.assertTrue(self.system.create_account(2, "account2"))

    def test_level_1_case_02_create_duplicate_account(self):
        self.assertTrue(self.system.create_account(1, "account1"))
        self.assertFalse(self.system.create_account(2, "account1"))
        self.assertTrue(self.system.create_account(3, "Account1"))

    def test_level_1_case_03_deposit(self):
        self.system.create_account(1, "account1")
        self.assertEqual(self.system.deposit(2, "account1", 1000), 1000)
        self.assertEqual(self.system.deposit(3, "account1", 500), 1500)

    def test_level_1_case_04_deposit_to_missing_account(self):
        self.system.create_account(1, "account1")
        self.assertIsNone(self.system.deposit(2, "account2", 1000))
        self.assertEqual(self.system.deposit(3, "account1", 1), 1)

    def test_level_1_case_05_transfer(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 2000)
        self.system.deposit(4, "account2", 100)
        self.assertEqual(self.system.transfer(5, "account1", "account2", 700), 1300)
        self.assertEqual(self.system.deposit(6, "account2", 1), 801)
        self.assertEqual(self.system.transfer(7, "account2", "account1", 801), 0)
        self.assertEqual(self.system.deposit(8, "account1", 1), 2102)

    def test_level_1_case_06_transfer_failures(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 500)
        self.assertIsNone(self.system.transfer(4, "account1", "account3", 100))
        self.assertIsNone(self.system.transfer(5, "account3", "account1", 100))
        self.assertIsNone(self.system.transfer(6, "account1", "account1", 100))
        self.assertIsNone(self.system.transfer(7, "account1", "account2", 501))
        self.assertIsNone(self.system.transfer(8, "account2", "account1", 1))
        self.assertEqual(self.system.transfer(9, "account1", "account2", 500), 0)

    def test_level_1_case_07_failed_transfer_changes_nothing(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 500)
        self.system.deposit(4, "account2", 200)
        self.assertIsNone(self.system.transfer(5, "account1", "account2", 1000))
        self.assertEqual(self.system.deposit(6, "account1", 1), 501)
        self.assertEqual(self.system.deposit(7, "account2", 1), 201)

    def test_level_1_case_08_transfer_exact_balance(self):
        self.system.create_account(1, "account1")
        self.system.create_account(2, "account2")
        self.system.deposit(3, "account1", 300)
        self.assertEqual(self.system.transfer(4, "account1", "account2", 300), 0)
        self.assertIsNone(self.system.transfer(5, "account1", "account2", 1))
        self.assertEqual(self.system.transfer(6, "account2", "account1", 150), 150)


if __name__ == "__main__":
    unittest.main()
