from modules.priority_queue import SortedPQ, UnsortedPQ
import sqlite3
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'



class SupplyMonitor:
    def __init__(self, use_sorted = True):
        self.db_name = "entries.db"
        if use_sorted:
            self._pq = SortedPQ()
        else:
            self._pq = UnsortedPQ()
         #use sorted PQ or Unsorted

        self.setup_db()
        self.load_db()
        
    def setup_db(self):
        connection = sqlite3.connect(self.db_name)

        cur = connection.cursor()
        _comm0 = """
                CREATE TABLE IF NOT EXISTS
                entries(
                _lgu TEXT UNIQUE,
                crop TEXT,
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
        
        _comm1 = "SELECT _lgu, crop, key FROM entries"
        cur.execute(_comm1)
        summary = cur.fetchall()
        connection.close()

        for _lgu, crop, key in summary:
            self._pq.insert(key, (crop, _lgu))
        ###
        ###

    def supply_checker(self, _lgu, crop, curr_supply, ideal_supply):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()

        imbalance = abs(curr_supply - ideal_supply) #Trun min-heap to max-heap PQ
        key = -imbalance

        _comm0 = """
                INSERT OR REPLACE INTO entries(_lgu, crop, key)
                VALUES(?, ?, ?)
                """

        cur.execute(_comm0, (_lgu, crop, key))

        connection.commit()
        connection.close()

        #LGU UPDATE/DUPLICATE
        self._pq.remove_lgu(_lgu)

        #set this as basis of your Priority Queue 
        self._pq.insert(key, (crop, _lgu)) #PQ ENTRY REPRESENTS: (<LGU>, <CROP>)

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
        _comm0 = "SELECT _lgu, crop, key FROM entries"

        cur.execute(_comm0)
        summary = cur.fetchall()

        connection.close()
        print("Priority Queue (in memory):")
        print(self._pq)

        print("\nDatabase Records:")
        for row in summary:
            lgu, crop, key = row
            print(f"LGU: {GREEN + BOLD + lgu + RESET}, Crop: {BOLD + crop}, Priority: {YELLOW}{-key}{RESET}")  # invert key for display

        return summary
