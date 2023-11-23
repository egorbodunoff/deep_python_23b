import sys
import logging.config


class Filter(logging.Filter):
    def filter(self, record):
        return len(record.msg.split()) % 2 == 0


def get_logging_dict():
    return {
        'version': 1,
        'formatters': {
            'stdout_formatter': {
                'format': 'stdout_log\t%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s',
            },
            'file_formatter': {
                'format': '\t%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s',
            },
        },
        'handlers': {
            'stream_handler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'stdout_formatter',
            },
            'file_handler': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'file_formatter',
                'filename': 'cache.log',
                'mode': 'w',
            },
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['file_handler'],
            },
            'stream_log': {
                "level": 'DEBUG',
                "handlers": ['stream_handler'],
            },

        },
    }


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

        log.debug(f'удаление из двусвязного списка элемента с ключом {elem.key}')

    def add(self, elem):
        elem.prev = self.right_elem.prev
        self.right_elem.prev.next = elem
        elem.next = self.right_elem
        self.right_elem.prev = elem

        log.debug(f'добавление в двусвязный список элемента с ключом {elem.key}')


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache_dict = {}
        self.dbl = DBList()

    def get(self, key):
        try:
            cur_el = self.cache_dict[key]

            self.dbl.remove(cur_el)
            self.dbl.add(cur_el)

            log.debug(f'get элемента {cur_el.key}, {cur_el.value}')
            return cur_el.value
        except KeyError:
            log.error(f'get несуществующего ключа {key}')
            return None

    def set(self, key, value):
        try:
            self.dbl.remove(self.cache_dict[key])
            elem = Link(key, value)
            self.cache_dict[key] = elem
            self.dbl.add(elem)

            log.debug(f'set существующего ключа {key}')
        except KeyError:
            elem = Link(key, value)
            self.cache_dict[key] = elem
            self.dbl.add(elem)

            log.debug(f'set несуществуещего ключа {key}')

            if len(self.cache_dict) > self.limit:
                drop_elem = self.dbl.left_elem.next
                self.dbl.remove(self.dbl.left_elem.next)
                del self.cache_dict[drop_elem.key]

                log.debug(f'превышена емкость, удаление элемента с ключом {drop_elem.key}')


if __name__ == '__main__':
    logging.config.dictConfig(get_logging_dict())

    log = logging.getLogger('stream_log') if '-s' in sys.argv else logging.getLogger()
    log.addFilter(Filter()) if '-f' in sys.argv else log
    cache = LRUCache(2)

    cache.set('k1', 'val1')
    cache.set('k2', 'val2')
    cache.set('k3', 'val3')
    cache.get('k30')
    cache.get('k2')
    cache.get('k1')
