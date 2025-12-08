from modules.priority_queue import SortedPQ, UnsortedPQ
import sqlite3



class SupplyMonitor:
    def __init__(self, use_sorted = True):
        self.db_name = "entries.db"
        if use_sorted:
            self._pq = SortedPQ()
        else:
            self._pq = UnsortedPQ()
         #use sorted PQ or Unsorted
        
    def setup_db(self):
        connection = sqlite3.connect(self.db_name)

        cur = connection.cursor()
        _comm0 = """
                CREATE TABLE IF NOT EXISTS
                entries(
                _lgu TEXT,
                key INTEGER
                )
                """
        cur.execute(_comm0)

        connection.commit()
        connection.close()

    def flush_db(self):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()

        cur.executescript("""DELETE FROM entries;
                    PRAGMA writable_schema = 0;
                    VACUUM;
                    PRAGMA integrity_check;
                    """)
        
        connection.commit()
        connection.close()

    def load_db(self):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
    
        ###
        ### LOAD FROM DB 
        
        _comm1 = "SELECT _lgu, key FROM entries"
        cur.execute(_comm1)
        summary = cur.fetchall()
        connection.close()

        for _lgu, key in summary:
            self._pq.insert(key, _lgu)
        ###
        ###



    def supply_checker(self, _lgu, curr_supply, ideal_supply):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()

        imbalance = abs(curr_supply - ideal_supply) #Trun min-heap to max-heap PQ
        key = -imbalance

        _comm0 = """
                INSERT INTO entries(_lgu, key)
                VALUES(?, ?)
                """
        



        cur.execute(_comm0, (_lgu, key))

        connection.commit()
        connection.close()

        #set this as basis of your Priority Queue
        
        self._pq.insert(key, _lgu)

    def remove_max(self):
        return self._pq.remove_min()

    def get_most_critical_LGU(self):
        if self._pq.is_empty():
            return None
        return self.remove_max() #removes highest priority
    
    def show_pq(self):
        # FIXED: use the same database used everywhere else
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()

        # FIXED SQL
        _comm0 = "SELECT _lgu, key FROM entries"

        cur.execute(_comm0)
        summary = cur.fetchall()

        connection.close()
        print("Priority Queue (in memory):")
        print(self._pq)

        print("\nDatabase Records:")
        for row in summary:
            print(f"LGU: {row[0]}, Priority: {-row[1]}")  # invert key for display

        return summary
    

