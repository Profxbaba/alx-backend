#!/usr/bin/env python3
"""
LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache is a caching system with a fixed size, using LIFO replacement.
    """

    def __init__(self):
        """
        Initialize the LIFOCache class.
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache with the given key.
        If key or item is None, do nothing.
        If the cache exceeds MAX_ITEMS, remove the most recently added item.

        :param key: The key associated with the item
        :param item: The item to be stored
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            self.order.append(key)
            self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                last_in_key = self.order.pop(-2)
                del self.cache_data[last_in_key]
                print(f"DISCARD: {last_in_key}")

    def get(self, key):
        """
        Get an item from the cache by key.
        If key is None or doesn't exist, return None.

        :param key: The key for the item to retrieve
        :return: The item associated with the key or None
        """
        return self.cache_data.get(key, None)
