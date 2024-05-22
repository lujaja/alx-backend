#!/usr/bin/env python3
""" Basic Dictionary
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class
    """
    def put(self, key, item):
        """ Function Put
            - Attributes:
                    key (key): parameter
                    item (value) parameter
        """
        if key is None or item is None:
            return
        self.cache_data.update({key: item})

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
