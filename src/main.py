from supply_monitor import SupplyMonitor 
import argparse as ap
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'



def main():
    monitor = SupplyMonitor(use_sorted=True)
    monitor.setup_db()
    parser = ap.ArgumentParser(description="POLARIS: Logistic System")



    parser.add_argument('--add', help="Add a new LGU", action="store_true")
    parser.add_argument('--cget', help="Get the most critical LGU", action="store_true")
    parser.add_argument('--list', help="List all the LGUs and Status", action="store_true")
    parser.add_argument('--flush', help="Fully resets your database", choices= ['true', 'false'])

    #args for adding a LGU
    parser.add_argument('--lgu', help="Add LGU name", type = str)
    parser.add_argument('--curr', help="Add the current supply in the LGU", type = int)
    parser.add_argument('--ideal', help="Add the ideal supply in the LGU", type = int)

    args = parser.parse_args()

    #adds LGU
    if args.add:
        if not (args.lgu and (args.curr is not None) and (args.ideal is not None)):
            print("Error: Please Complete the format -> --lgu [lgu] --curr_supply[int] --ideal_supply[int]")
            return
        monitor.supply_checker(args.lgu, args.curr, args.ideal)
        print(f"Added {RED + BOLD + args.lgu + RESET} successfully.")


        
    #list of entries 
    if args.list:
        monitor.load_db()
        monitor.show_pq()
    #gets most crit lgu
    if args.cget:        
        monitor.load_db()
        most = monitor.get_most_critical_LGU()
        if most is None:
            print("No LGUs in queue. Add Some?")
        else:
            print(f"Most critical LGU: {RED + BOLD + most + RESET}")

    if args.flush:
        print("Reseting...")
        monitor.flush_db()


    #prints the current standing of priority list
if __name__ == "__main__":
    main()