#!/usr/bin/env python3
""" LIFO caching
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class
    """
    def __init__(self):
        """ Initializer
        """
        super().__init__()
        self.lifo_order = []

    def put(self, key, item):
        """ Function Put
            - Attributes:
                    key (key): parameter
                    item (value) parameter
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.lifo_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = self.lifo_order.pop()
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

        self.cache_data[key] = item
        self.lifo_order.append(key)

    def get(self, key):
        """
        get Function
        Attributes:
            key (key): parameter
        Return:
            value linked to the key
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
