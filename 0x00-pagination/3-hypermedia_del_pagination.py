#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Any


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
                i: truncated_dataset[i] for i in range(len(truncated_dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict[str, Any]:
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
        assert 0 <= index < len(indexed_dataset), "Index out of range."

        page_data = []
        current_index = index
        count = 0

        while count < page_size and current_index < len(indexed_dataset):
            if current_index in indexed_dataset:
                page_data.append(indexed_dataset[current_index])
                count += 1
            current_index += 1

        next_index = current_index

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': page_data
        }
