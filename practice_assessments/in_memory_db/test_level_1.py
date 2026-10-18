import unittest

from in_memory_db_impl import InMemoryDBImpl


class Level1Tests(unittest.TestCase):

    def setUp(self):
        self.db = InMemoryDBImpl()

    def test_level_1_case_01_set_and_get(self):
        self.assertIsNone(self.db.set("user1", "name", "Ada"))
        self.db.set("user1", "city", "London")
        self.assertEqual(self.db.get("user1", "name"), "Ada")
        self.assertEqual(self.db.get("user1", "city"), "London")

    def test_level_1_case_02_get_missing(self):
        self.db.set("user1", "name", "Ada")
        self.assertIsNone(self.db.get("user2", "name"))
        self.assertIsNone(self.db.get("user1", "city"))

    def test_level_1_case_03_set_overwrites(self):
        self.db.set("user1", "name", "Ada")
        self.db.set("user1", "name", "Grace")
        self.assertEqual(self.db.get("user1", "name"), "Grace")

    def test_level_1_case_04_records_are_independent(self):
        self.db.set("user1", "name", "Ada")
        self.db.set("user2", "name", "Grace")
        self.assertEqual(self.db.get("user1", "name"), "Ada")
        self.assertEqual(self.db.get("user2", "name"), "Grace")
        self.db.set("user2", "name", "Alan")
        self.assertEqual(self.db.get("user1", "name"), "Ada")

    def test_level_1_case_05_same_name_for_key_and_field(self):
        self.db.set("name", "name", "key")
        self.db.set("key", "name", "value")
        self.assertEqual(self.db.get("name", "name"), "key")
        self.assertEqual(self.db.get("key", "name"), "value")
        self.assertIsNone(self.db.get("name", "key"))

    def test_level_1_case_06_delete(self):
        self.db.set("user1", "name", "Ada")
        self.db.set("user1", "city", "London")
        self.assertTrue(self.db.delete("user1", "name"))
        self.assertIsNone(self.db.get("user1", "name"))
        self.assertEqual(self.db.get("user1", "city"), "London")

    def test_level_1_case_07_delete_missing(self):
        self.db.set("user1", "name", "Ada")
        self.assertFalse(self.db.delete("user2", "name"))
        self.assertFalse(self.db.delete("user1", "city"))
        self.assertTrue(self.db.delete("user1", "name"))
        self.assertFalse(self.db.delete("user1", "name"))

    def test_level_1_case_08_set_after_delete(self):
        self.db.set("user1", "name", "Ada")
        self.assertTrue(self.db.delete("user1", "name"))
        self.assertIsNone(self.db.get("user1", "name"))
        self.db.set("user1", "name", "Grace")
        self.assertEqual(self.db.get("user1", "name"), "Grace")


if __name__ == "__main__":
    unittest.main()
