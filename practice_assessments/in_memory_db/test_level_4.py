import unittest

from in_memory_db_impl import InMemoryDBImpl


class Level4Tests(unittest.TestCase):

    def setUp(self):
        self.db = InMemoryDBImpl()

    def test_level_4_case_01_backup_counts_records(self):
        self.assertEqual(self.db.backup(1), 0)
        self.db.set_at(2, "user1", "name", "Ada")
        self.db.set_at_with_ttl(3, "user2", "token", "abc", 5)
        self.db.set_at(4, "user3", "x", "1")
        self.assertTrue(self.db.delete_at(5, "user3", "x"))
        self.assertEqual(self.db.backup(6), 2)
        self.assertEqual(self.db.backup(8), 1)

    def test_level_4_case_02_restore(self):
        self.db.set_at(1, "user1", "name", "Ada")
        self.db.set_at(2, "user1", "city", "London")
        self.assertEqual(self.db.backup(3), 1)
        self.db.set_at(4, "user1", "name", "Grace")
        self.assertTrue(self.db.delete_at(5, "user1", "city"))
        self.db.set_at(6, "user2", "name", "Alan")
        self.assertIsNone(self.db.restore(7, 3))
        self.assertEqual(self.db.get_at(8, "user1", "name"), "Ada")
        self.assertEqual(self.db.scan_at(9, "user1"), ["city(London)", "name(Ada)"])
        self.assertEqual(self.db.scan_at(10, "user2"), [])

    def test_level_4_case_03_restore_picks_latest_backup_at_or_before(self):
        self.db.set_at(1, "user1", "v", "1")
        self.db.backup(2)
        self.db.set_at(3, "user1", "v", "2")
        self.db.backup(4)
        self.db.set_at(5, "user1", "v", "3")
        self.db.backup(6)
        self.db.set_at(7, "user1", "v", "4")
        self.db.restore(8, 4)
        self.assertEqual(self.db.get_at(9, "user1", "v"), "2")
        self.db.restore(10, 5)
        self.assertEqual(self.db.get_at(11, "user1", "v"), "2")
        self.db.restore(12, 2)
        self.assertEqual(self.db.get_at(13, "user1", "v"), "1")
        self.db.restore(14, 13)
        self.assertEqual(self.db.get_at(15, "user1", "v"), "3")

    def test_level_4_case_04_restore_recalculates_ttl(self):
        self.db.set_at_with_ttl(1, "user1", "token", "abc", 10)
        self.assertEqual(self.db.backup(4), 1)
        self.db.restore(20, 4)
        self.assertEqual(self.db.get_at(26, "user1", "token"), "abc")
        self.assertIsNone(self.db.get_at(27, "user1", "token"))

    def test_level_4_case_05_expired_fields_are_not_backed_up(self):
        self.db.set_at_with_ttl(1, "user1", "a", "1", 4)
        self.db.set_at_with_ttl(2, "user1", "b", "2", 10)
        self.assertEqual(self.db.backup(5), 1)
        self.db.restore(20, 5)
        self.assertEqual(self.db.scan_at(21, "user1"), ["b(2)"])
        self.assertEqual(self.db.get_at(26, "user1", "b"), "2")
        self.assertIsNone(self.db.get_at(27, "user1", "b"))

    def test_level_4_case_06_restore_keeps_fields_without_ttl(self):
        self.db.set_at(1, "user1", "name", "Ada")
        self.db.backup(2)
        self.db.set_at_with_ttl(3, "user1", "name", "Grace", 5)
        self.db.restore(4, 2)
        self.assertEqual(self.db.get_at(1000000, "user1", "name"), "Ada")

    def test_level_4_case_07_backups_are_unaffected_by_later_changes(self):
        self.db.set_at(1, "user1", "name", "Ada")
        self.db.set_at(2, "user1", "city", "London")
        self.db.backup(3)
        self.db.set_at(4, "user1", "name", "Grace")
        self.assertTrue(self.db.delete_at(5, "user1", "city"))
        self.db.restore(6, 3)
        self.assertEqual(self.db.scan_at(7, "user1"), ["city(London)", "name(Ada)"])
        self.db.set_at(8, "user1", "name", "Alan")
        self.assertTrue(self.db.delete_at(9, "user1", "city"))
        self.db.set_at(10, "user2", "x", "1")
        self.db.restore(11, 3)
        self.assertEqual(self.db.scan_at(12, "user1"), ["city(London)", "name(Ada)"])
        self.assertEqual(self.db.scan_at(13, "user2"), [])

    def test_level_4_case_08_backup_after_restore(self):
        self.db.set_at(1, "user1", "v", "A")
        self.assertEqual(self.db.backup(2), 1)
        self.db.set_at(3, "user1", "v", "B")
        self.assertEqual(self.db.backup(4), 1)
        self.db.restore(5, 3)
        self.assertEqual(self.db.backup(6), 1)
        self.db.set_at(7, "user1", "v", "C")
        self.db.restore(8, 4)
        self.assertEqual(self.db.get_at(9, "user1", "v"), "B")
        self.db.restore(10, 7)
        self.assertEqual(self.db.get_at(11, "user1", "v"), "A")

    def test_level_4_case_09_ttl_across_repeated_restores(self):
        self.db.set_at_with_ttl(1, "user1", "token", "abc", 10)
        self.db.backup(3)
        self.db.restore(5, 3)
        self.db.backup(7)
        self.db.restore(20, 7)
        self.assertEqual(self.db.get_at(25, "user1", "token"), "abc")
        self.assertIsNone(self.db.get_at(26, "user1", "token"))


if __name__ == "__main__":
    unittest.main()
