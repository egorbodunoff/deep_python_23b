import unittest

from lru_cache import LRUCache


class TestMetaClass(unittest.TestCase):
    def test_base(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

    def test_one_el(self):
        cache = LRUCache(1)

        cache.set('k1', 'val1')
        self.assertEqual(cache.get('k1'), 'val1')

        cache.set('k2', 'val2')
        self.assertEqual(cache.get('k1'), None)
        self.assertEqual(cache.get('k2'), 'val2')

    def test_change_val(self):
        cache = LRUCache(2)

        cache.set('k1', 'val1')
        cache.set('k2', 'val2')
        self.assertEqual(cache.cache_dict['k1'].prev, cache.dbl.left_elem)
        self.assertEqual(cache.cache_dict['k1'].next, cache.cache_dict['k2'])

        cache.set('k1', 'val3')
        self.assertEqual(cache.cache_dict['k1'].value, 'val3')
        self.assertEqual(cache.cache_dict['k1'].next, cache.dbl.right_elem)
        self.assertEqual(cache.cache_dict['k1'].prev, cache.cache_dict['k2'])

        self.assertEqual(cache.get('k1'), 'val3')

    def test_change_val_full(self):
        cache = LRUCache(2)

        cache.set('k1', 'val1')
        cache.set('k2', 'val2')
        cache.set('k2', 'changed val')

        self.assertEqual(cache.get('k1'), 'val1')
        self.assertEqual(cache.get('k2'), 'changed val')

    def test_links(self):
        cache = LRUCache(2)

        cache.set('k1', 'val1')
        cache.set('k2', 'val2')
        self.assertEqual(cache.cache_dict['k1'].next, cache.cache_dict['k2'])

        cache.get('k1')
        self.assertEqual(cache.cache_dict['k2'].next, cache.cache_dict['k1'])

    def test_err(self):
        cache = LRUCache(2)
        cache.set('k1', 'val1')
        cache.set('k2', 'val2')

        cache.set('k3', 'val3')

        with self.assertRaises(KeyError) as err:
            print(cache.cache_dict['k1'])

        self.assertEqual(type(err.exception), KeyError)
