class Link:
    def __init__(self, key, value):
        self.key = key
        self.value = value

        self.next = None
        self.prev = None


class DBList:
    def __init__(self):
        self.right_elem = Link(None, None)
        self.left_elem = Link(None, None)

        self.right_elem.prev = self.left_elem
        self.left_elem.next = self.right_elem

    @staticmethod
    def remove(elem):
        elem.next.prev, elem.prev.next = elem.prev, elem.next

    def add(self, elem):
        elem.prev = self.right_elem.prev
        self.right_elem.prev.next = elem
        elem.next = self.right_elem
        self.right_elem.prev = elem


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache_dict = {}
        self.dbl = DBList()

    def get(self, key):
        value = None

        if key in self.cache_dict:
            cur_el = self.cache_dict[key]
            value = cur_el.value

            self.dbl.remove(cur_el)
            self.dbl.add(cur_el)

        return value

    def set(self, key, value):
        if key in self.cache_dict:
            self.dbl.remove(self.cache_dict[key])

        elem = Link(key, value)
        self.cache_dict[key] = elem
        self.dbl.add(elem)

        if len(self.cache_dict) > self.limit:
            drop_elem = self.dbl.left_elem.next

            self.dbl.remove(self.dbl.left_elem.next)
            del self.cache_dict[drop_elem.key]
