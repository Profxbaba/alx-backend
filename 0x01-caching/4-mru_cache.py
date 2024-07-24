#!/usr/bin/env python3
"""
MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache is a caching system with a fixed size, using MRU replacement.
    """

    def __init__(self):
        """
        Initialize the MRUCache class.
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache with the given key.
        If key or item is None, do nothing.
        If the cache exceeds MAX_ITEMS, remove the most recently used item.

        :param key: The key associated with the item
        :param item: The item to be stored
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.order.pop()
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")

            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """
        Get an item from the cache by key.
        If key is None or doesn't exist, return None.

        :param key: The key for the item to retrieve
        :return: The item associated with the key or None
        """
        if key is None or key not in self.cache_data:
            return None
        # Update the order to mark key as recently used
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
