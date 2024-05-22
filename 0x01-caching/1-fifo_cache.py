#!/usr/bin/env python3
""" FIFO caching
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class
    """
    def __init__(self):
        """ Initializer
        """
        super().__init__()

    def put(self, key, item):
        """ Function Put
            - Attributes:
                    key (key): parameter
                    item (value) parameter
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

        key_list = list(self.cache_data.keys())
        if len(key_list) > BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(key_list[0]))
            del self.cache_data[key_list[0]]

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
