#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict  # Import Dict type from typing module


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """
        Returns a dictionary with pagination information and dataset page.

        Args:
            index (int): Current start index of the return page.
                         Defaults to 0.
            page_size (int): Current page size. Defaults to 10.

        Returns:
            dict: Contains the following keys:
                  - index: Current start index of the return page.
                  - next_index: Next index to query with.
                  - page_size: Current page size.
                  - data: Actual page of the dataset.
        """
        indexed_dataset = self.indexed_dataset()
        assert index >= 0 and index < len(indexed_dataset), "Index out of range"

        current_index = index
        next_index = current_index + page_size

        if next_index > len(indexed_dataset):
            next_index = len(indexed_dataset)

        # Retrieve page data, handling possible KeyError
        page_data = []
        for i in range(current_index, next_index):
            if i in indexed_dataset:
                page_data.append(indexed_dataset[i])

        return {
            'index': current_index,
            'next_index': next_index,
            'page_size': page_size,
            'data': page_data
        }
