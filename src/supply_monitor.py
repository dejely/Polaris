from modules.priority_queue import SortedPQ, UnsortedPQ
import numpy as py
import argparse
from datetime import datetime

class SupplyMonitor:
    def __init__(self, use_sorted = True):
        self._pq = SortedPQ() if use_sorted else UnsortedPQ() #use sorted PQ or Unsorted

    def supply_checker(self, _LGU, curr_supply, ideal_supply):
        imbalance = abs(curr_supply - ideal_supply)

        #set this as basis of your Priority Queue
        #Trun min-heap to max-heap PQ
        key = -imbalance

        self._pq.insert(key, _LGU)

    def remove_max(self):
        return self._pq.remove_min()

    def get_most_critical_LGU(self):
        if self._pq.is_empty():
            return None
        return self.remove_max() #removes highest priority


