#!/usr/bin/env python3
"""
BasicCache module
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache is a caching system with no limit.
    It inherits from BaseCaching and implements a simple
    put and get method without a limit on cache size.
    """

    def put(self, key, item):
        """
        Add an item in the cache with the given key.
        If key or item is None, do nothing.

        :param key: The key associated with the item
        :param item: The item to be stored
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item from the cache by key.
        If key is None or doesn't exist, return None.

        :param key: The key for the item to retrieve
        :return: The item associated with the key or None
        """
        return self.cache_data.get(key, None)
