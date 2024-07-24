#!/usr/bin/env python3
"""
LFUCache module.
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache is a caching system that uses the Least Frequently Used (LFU)
    algorithm for item eviction. In case of ties, the Least Recently Used (LRU)
    algorithm is used to determine which item to remove.
    """

    def __init__(self):
        """
        Initialize the LFUCache class.
        """
        super().__init__()
        self.usage_count = defaultdict(int)
        self.order = OrderedDict()

    def put(self, key, item):
        """
        Add an item to the cache with the specified key. If the key or item
        is None, do nothing. If the cache exceeds MAX_ITEMS, remove the least
        frequently used item. In case of ties, use LRU eviction.

        Args:
            key (str): The key associated with the item.
            item (any): The item to be stored.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.usage_count[key] += 1
            self.order.move_to_end(key)
            self.cache_data[key] = item
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu_key = self._get_lfu_key()
                if lfu_key:
                    del self.cache_data[lfu_key]
                    del self.usage_count[lfu_key]
                    self.order.pop(lfu_key)
                    print(f"DISCARD: {lfu_key}")

            self.cache_data[key] = item
            self.usage_count[key] = 1
            self.order[key] = item

    def get(self, key):
        """
        Retrieve an item from the cache by key. If the key is None or doesn't
        exist, return None. Update the usage count and mark the key as used.

        Args:
            key (str): The key for the item to retrieve.

        Returns:
            any: The item associated with the key or None.
        """
        if key is None or key not in self.cache_data:
            return None

        self.usage_count[key] += 1
        self.order.move_to_end(key)
        return self.cache_data[key]

    def _get_lfu_key(self):
        """
        Find the least frequently used key in the cache. If there are multiple
        keys with the same frequency, use LRU eviction.

        Returns:
            str: The key of the least frequently used item.
        """
        min_freq = min(self.usage_count.values(), default=None)
        if min_freq is None:
            return None

        lfu_keys = [key for key, freq in self.usage_count.items()
                    if freq == min_freq]
        if len(lfu_keys) == 1:
            return lfu_keys[0]

        # In case of tie, use LRU to determine which to discard
        lru_key = next(iter(self.order))
        return lru_key
