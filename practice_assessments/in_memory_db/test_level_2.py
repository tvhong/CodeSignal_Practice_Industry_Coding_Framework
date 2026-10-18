import unittest

from in_memory_db_impl import InMemoryDBImpl


class Level2Tests(unittest.TestCase):

    def setUp(self):
        self.db = InMemoryDBImpl()

    def test_level_2_case_01_scan(self):
        self.db.set("user1", "name", "Ada")
        self.db.set("user1", "city", "London")
        self.db.set("user1", "age", "36")
        self.assertEqual(self.db.scan("user1"), ["age(36)", "city(London)", "name(Ada)"])

    def test_level_2_case_02_scan_missing_record(self):
        self.db.set("user1", "name", "Ada")
        self.assertEqual(self.db.scan("user2"), [])

    def test_level_2_case_03_scan_reflects_changes(self):
        self.db.set("user1", "name", "Ada")
        self.db.set("user1", "city", "London")
        self.db.set("user1", "name", "Grace")
        self.assertEqual(self.db.scan("user1"), ["city(London)", "name(Grace)"])
        self.assertTrue(self.db.delete("user1", "city"))
        self.assertEqual(self.db.scan("user1"), ["name(Grace)"])
        self.assertTrue(self.db.delete("user1", "name"))
        self.assertEqual(self.db.scan("user1"), [])

    def test_level_2_case_04_scan_only_its_own_record(self):
        self.db.set("user1", "name", "Ada")
        self.db.set("user2", "city", "Paris")
        self.assertEqual(self.db.scan("user1"), ["name(Ada)"])
        self.assertEqual(self.db.scan("user2"), ["city(Paris)"])

    def test_level_2_case_05_scan_sorts_alphabetically_not_by_insertion(self):
        self.db.set("user1", "b", "2")
        self.db.set("user1", "a10", "3")
        self.db.set("user1", "a2", "1")
        self.db.set("user1", "B", "4")
        self.assertEqual(self.db.scan("user1"), ["B(4)", "a10(3)", "a2(1)", "b(2)"])

    def test_level_2_case_06_scan_by_prefix(self):
        self.db.set("user1", "phone_home", "111")
        self.db.set("user1", "phone_work", "222")
        self.db.set("user1", "name", "Ada")
        self.db.set("user1", "phone", "333")
        self.assertEqual(
            self.db.scan_by_prefix("user1", "phone"),
            ["phone(333)", "phone_home(111)", "phone_work(222)"],
        )
        self.assertEqual(self.db.scan_by_prefix("user1", "phone_"), ["phone_home(111)", "phone_work(222)"])
        self.assertEqual(self.db.scan_by_prefix("user1", "n"), ["name(Ada)"])

    def test_level_2_case_07_scan_by_prefix_no_match(self):
        self.db.set("user1", "name", "Ada")
        self.assertEqual(self.db.scan_by_prefix("user1", "city"), [])
        self.assertEqual(self.db.scan_by_prefix("user1", "names"), [])
        self.assertEqual(self.db.scan_by_prefix("user2", "n"), [])

    def test_level_2_case_08_scan_by_prefix_is_case_sensitive(self):
        self.db.set("user1", "Name", "Ada")
        self.db.set("user1", "name", "Grace")
        self.assertEqual(self.db.scan_by_prefix("user1", "N"), ["Name(Ada)"])
        self.assertEqual(self.db.scan_by_prefix("user1", "n"), ["name(Grace)"])

    def test_level_2_case_09_scan_by_prefix_matches_field_not_value(self):
        self.db.set("user1", "name", "phone")
        self.db.set("user1", "phone", "123")
        self.assertEqual(self.db.scan_by_prefix("user1", "phone"), ["phone(123)"])


if __name__ == "__main__":
    unittest.main()
