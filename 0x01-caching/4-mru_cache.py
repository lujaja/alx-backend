#!/usr/bin/env python3
""" LRU caching"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class"""
    def __init__(self):
        """
        Initializes the MRUCache object.

        This method initializes the MRUCache object by
         calling the __init__ method.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Adds an item to the cache with the given key.
        If the key already exists in the cache,
        :param key: The key to associate with the item.
        :type key: Any hashable type.
        :param item: The item to add to the cache.
        :type item: Any type.
        :return: None.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data.move_to_end(key)

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key, _ = self.cache_data.popitem(last=True)
            print("DISCARD: {}".format(lru_key))

        self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves the value associated with the given key from the cache.

        Parameters:
            key (Any): The key to search for in the cache.

        Returns:
            Any: The value associated with the key, or None if the
            key is not found in the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        self.cache_data.move_to_end(key)
        return self.cache_data[key]
