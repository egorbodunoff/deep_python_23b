import unittest

from lru_cache import LRUCache


class TestMetaClass(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = LRUCache(2)
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

    def test_base(self):
        self.assertEqual(self.cache.get("k3"), None)
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k1"), "val1")

        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "val1")

    def test_links(self):
        self.assertEqual(self.cache.cache_dict["k1"].next, self.cache.cache_dict["k2"])
        self.cache.get("k1")
        self.assertNotEqual(self.cache.cache_dict["k1"].next, self.cache.cache_dict["k2"])

    def test_err(self):
        self.cache.set("k3", "val3")

        with self.assertRaises(KeyError) as err:
            print(self.cache.cache_dict["k1"])

        self.assertEqual(type(err.exception), KeyError)

