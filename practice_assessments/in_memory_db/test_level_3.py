import unittest

from in_memory_db_impl import InMemoryDBImpl


class Level3Tests(unittest.TestCase):

    def setUp(self):
        self.db = InMemoryDBImpl()

    def test_level_3_case_01_timestamped_basics(self):
        self.assertIsNone(self.db.set_at(1, "user1", "name", "Ada"))
        self.db.set_at(2, "user1", "city", "London")
        self.assertEqual(self.db.get_at(3, "user1", "name"), "Ada")
        self.assertEqual(self.db.scan_at(4, "user1"), ["city(London)", "name(Ada)"])
        self.assertEqual(self.db.scan_by_prefix_at(5, "user1", "c"), ["city(London)"])
        self.assertTrue(self.db.delete_at(6, "user1", "city"))
        self.assertFalse(self.db.delete_at(7, "user1", "city"))
        self.assertIsNone(self.db.get_at(8, "user2", "name"))

    def test_level_3_case_02_ttl_expires_at_boundary(self):
        self.assertIsNone(self.db.set_at_with_ttl(10, "user1", "token", "abc", 5))
        self.assertEqual(self.db.get_at(11, "user1", "token"), "abc")
        self.assertEqual(self.db.get_at(14, "user1", "token"), "abc")
        self.assertIsNone(self.db.get_at(15, "user1", "token"))
        self.assertIsNone(self.db.get_at(100, "user1", "token"))

    def test_level_3_case_03_expired_fields_are_hidden_from_scans(self):
        self.db.set_at(1, "user1", "name", "Ada")
        self.db.set_at_with_ttl(2, "user1", "token", "abc", 10)
        self.db.set_at_with_ttl(3, "user1", "tmp", "x", 3)
        self.assertEqual(self.db.scan_at(5, "user1"), ["name(Ada)", "tmp(x)", "token(abc)"])
        self.assertEqual(self.db.scan_at(6, "user1"), ["name(Ada)", "token(abc)"])
        self.assertEqual(self.db.scan_by_prefix_at(7, "user1", "t"), ["token(abc)"])
        self.assertEqual(self.db.scan_at(12, "user1"), ["name(Ada)"])
        self.assertEqual(self.db.scan_by_prefix_at(13, "user1", "t"), [])

    def test_level_3_case_04_delete_expired_field(self):
        self.db.set_at_with_ttl(1, "user1", "token", "abc", 10)
        self.assertFalse(self.db.delete_at(11, "user1", "token"))
        self.db.set_at_with_ttl(12, "user1", "token", "def", 10)
        self.assertTrue(self.db.delete_at(21, "user1", "token"))
        self.assertIsNone(self.db.get_at(22, "user1", "token"))

    def test_level_3_case_05_set_at_removes_ttl(self):
        self.db.set_at_with_ttl(1, "user1", "token", "abc", 10)
        self.db.set_at(5, "user1", "token", "def")
        self.assertEqual(self.db.get_at(11, "user1", "token"), "def")
        self.assertEqual(self.db.get_at(1000000, "user1", "token"), "def")

    def test_level_3_case_06_set_with_ttl_replaces_expiry(self):
        self.db.set_at_with_ttl(1, "user1", "token", "abc", 10)
        self.db.set_at_with_ttl(5, "user1", "token", "def", 20)
        self.assertEqual(self.db.get_at(11, "user1", "token"), "def")
        self.assertEqual(self.db.get_at(24, "user1", "token"), "def")
        self.assertIsNone(self.db.get_at(25, "user1", "token"))

    def test_level_3_case_07_shorter_ttl_also_replaces_expiry(self):
        self.db.set_at(1, "user1", "name", "Ada")
        self.db.set_at_with_ttl(2, "user1", "name", "Grace", 3)
        self.assertEqual(self.db.get_at(4, "user1", "name"), "Grace")
        self.assertIsNone(self.db.get_at(5, "user1", "name"))
        self.assertEqual(self.db.scan_at(6, "user1"), [])

    def test_level_3_case_08_set_after_expiry(self):
        self.db.set_at_with_ttl(1, "user1", "token", "abc", 5)
        self.assertIsNone(self.db.get_at(6, "user1", "token"))
        self.db.set_at(7, "user1", "token", "def")
        self.assertEqual(self.db.get_at(8, "user1", "token"), "def")
        self.assertEqual(self.db.scan_at(9, "user1"), ["token(def)"])

    def test_level_3_case_09_ttls_are_per_field(self):
        self.db.set_at_with_ttl(1, "user1", "a", "1", 10)
        self.db.set_at_with_ttl(2, "user1", "b", "2", 5)
        self.db.set_at_with_ttl(3, "user2", "a", "3", 2)
        self.assertEqual(self.db.scan_at(5, "user1"), ["a(1)", "b(2)"])
        self.assertEqual(self.db.scan_at(6, "user2"), [])
        self.assertEqual(self.db.scan_at(7, "user1"), ["a(1)"])
        self.assertEqual(self.db.get_at(10, "user1", "a"), "1")
        self.assertIsNone(self.db.get_at(11, "user1", "a"))


if __name__ == "__main__":
    unittest.main()
