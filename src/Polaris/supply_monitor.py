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
        self.crops = {}
        self.load_db()
        
        
    def setup_db(self):
        connection = sqlite3.connect(self.db_name)
        connection.close()

    def create_crop_table(self, crop):
        table = crop.lower()
        #setup a new table for a new type of crop
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()

        _comm0 = f"""
                CREATE TABLE IF NOT EXISTS {table}(
                _lgu TEXT UNIQUE,
                key INTEGER
                );
                """
        cur.execute(_comm0)

        connection.commit()
        connection.close()

    def flush_db(self):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
       
        cur.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """)
        tables = [t[0] for t in cur.fetchall()]
        for table in tables:
            cur.execute(f"DELETE FROM {table}")
        
        connection.commit()
        connection.execute("VACUUM")
        connection.close()
        self.crops = {} #reset in memory

    def load_db(self):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'") #get all tables from DB
        tables = [t[0] for t in cur.fetchall()]

        for table in tables:
            crop = table.capitalize()

        ### LOAD FROM DB 
            if crop not in self.crops:
                self.crops[crop] = SortedPQ()

            cur.execute(f"SELECT _lgu, key FROM {table}")

            for _lgu, key in cur.fetchall():
                self.crops[crop].insert(key, (_lgu, crop))
            
        connection.close()

    def supply_checker(self, _lgu, crop, curr_supply, ideal_supply):
        #validation catch
        if crop is None or crop.strip() == "":
            raise ValueError("Crop cannot be empty. Use --crop <name>.")
        
        self.create_crop_table(crop)
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        table = crop.lower()

        imbalance = curr_supply - ideal_supply #Trun min-heap to max-heap PQ
        key = -imbalance

        _comm0 = f"""
                INSERT OR REPLACE INTO {table}(_lgu, key)
                VALUES(?, ?)
                """

        cur.execute(_comm0, (_lgu, key))
        connection.commit()
        connection.close()

        if crop not in self.crops:
            self.crops[crop] = SortedPQ()

        #LGU UPDATE/DUPLICATE
       

        #set this as basis of your Priority Queue 
        self.crops[crop].insert(key, (_lgu, crop)) #PQ ENTRY REPRESENTS: (<LGU>, <CROP>)

    def remove_max(self):
        return self._pq.remove_min()

    def get_most_critical_LGU(self):
        if self._pq.is_empty():
            return None
        return self.remove_max() #removes highest priority
    
    def show_pq(self):
        print("\n=== Priority Queues by Crop ===")

        # Print in-memory PQs
        for crop, pq in self.crops.items():
            if crop is None:
                continue

            print(f"\nCrop: {YELLOW}{crop}{RESET}")
            print(pq)

        # Print DB records
        print("\n=== Database Records ===")

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cur.fetchall()]

        for table in tables:
            if table.startswith("sqlite_"):
                continue

            crop = table.capitalize()
            print(f"\nTable: {crop}")

            cur.execute(f"SELECT _lgu, key FROM {table}") #find on crop tablee
            
            for lgu, key in cur.fetchall():
                print(f"  LGU: {GREEN}{lgu}{RESET} | Priority: {YELLOW}{key}{RESET}")

        conn.close()

    def match_supply(self, crop):
        # Defensive validation
        if not crop:
            print("Error: No crop name provided.")
            return None

        crop = crop.capitalize()

        pq = self.crops.get(crop)
        if not pq or pq.size < 2:
            print(f"Not enough LGUs to match for crop '{crop}'.")
            return None

        # Convert PQ to list of dicts
        entries = pq.to_object()

        # Shortage = most negative priority → index 0
        shortage = entries[0]

        # Oversupply = most positive priority → index -1
        oversupply = entries[-1]

        # Avoid matching the same LGU
        if shortage["lgu"] == oversupply["lgu"]:
            print("Cannot match: Only one LGU present.")
            return None

        return shortage, oversupply
