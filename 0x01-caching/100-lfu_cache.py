#!/usr/bin/env python3
"""
LFU caching
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    Difine class LFUCache
    """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()
        self.cache_data = {}
        self.usage_frequency = {}
        self.access_order = OrderedDict()

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.usage_frequency[key] += 1
            self.access_order.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.usage_frequency.values())
                lfu_keys = [
                    k for k,
                    v in self.usage_frequency.items() if v == min_freq
                ]
                if len(lfu_keys) > 1:
                    lru_key = next(
                        k for k in self.access_order if k in lfu_keys
                    )
                else:
                    lru_key = lfu_keys[0]
                del self.cache_data[lru_key]
                del self.usage_frequency[lru_key]
                del self.access_order[lru_key]
                print("DISCARD: {}".format(lru_key))

            self.cache_data[key] = item
            self.usage_frequency[key] = 1
            self.access_order[key] = None

    def get(self, key):
        """
        Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self.usage_frequency[key] += 1
        self.access_order.move_to_end(key)
        return self.cache_data[key]
