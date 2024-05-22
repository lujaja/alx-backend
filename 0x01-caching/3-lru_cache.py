#!/usr/bin/env python3
""" LRU caching
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class
    """
    def __init__(self):
        """ Initializer
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Function Put
            - Attributes:
                    key (key): parameter
                    item (value) parameter
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key, _ = self.cache_data.popitem(last=False)
            print("DISCARD: {}".format(lru_key))

        self.cache_data[key] = item

    def get(self, key):
        """ Function Get
            - Attributes:
                    key (key): parameter
        """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.move_to_end(key)
        return self.cache_data.get(key)
