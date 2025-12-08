from modules.priority_queue import SortedPQ, UnsortedPQ



class SupplyMonitor:
    def __init__(self, use_sorted = True):
        if use_sorted:
            self._pq = SortedPQ()
        else:
            self._pq = UnsortedPQ()
         #use sorted PQ or Unsorted

    def supply_checker(self, _lgu, curr_supply, ideal_supply):
        imbalance = abs(curr_supply - ideal_supply)

        #set this as basis of your Priority Queue
        #Trun min-heap to max-heap PQ
        key = -imbalance

        self._pq.insert(key, _lgu)

    def remove_max(self):
        return self._pq.remove_min()

    def get_most_critical_LGU(self):
        if self._pq.is_empty():
            return None
        return self.remove_max() #removes highest priority
    
    def show_pq(self):
        print(self._pq)


