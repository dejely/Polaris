from .supply_monitor import SupplyMonitor 
import argparse as ap
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'


def main():
    monitor = SupplyMonitor(use_sorted=True)

    parser = ap.ArgumentParser(description="POLARIS: Logistic System")

    parser.add_argument('--add', help="Add a new LGU", action="store_true")
    parser.add_argument('--cget', help="Get the most critical LGU", action="store_true")
    parser.add_argument('--list', help="List all the LGUs and Status", action="store_true")
    parser.add_argument('--flush', help="Fully resets your database", choices= ['true', 'false'])
    parser.add_argument('--match', help="Matches Oversupply to Undersupply", action="store_true")
    

    #args for adding a LGU
    parser.add_argument('--lgu', help="Add LGU name", type = str)
    parser.add_argument('--crop', help="Crop type", type=str)
    parser.add_argument('--curr', help="Add the current supply in the LGU", type = int)
    parser.add_argument('--ideal', help="Add the ideal supply in the LGU", type = int)

    args = parser.parse_args()

    #adds LGU
    if args.add:
        if not (args.lgu and args.crop and (args.curr is not None) and (args.ideal is not None)):
            print("Error: Please Complete the format -> --lgu [lgu] --crop [crop] --curr_supply[int] --ideal_supply[int]")
            return
        monitor.supply_checker(args.lgu, args.crop, args.curr, args.ideal)
        print(f"Added {RED + BOLD + args.lgu + RESET} with Crop {BOLD + args.crop + RESET} successfully.")
        
    if args.match:
        if not args.crop:
            print("Error: --match requires --crop <CropName>")
            return
        result = monitor.match_supply(args.crop)

        Oversupply, Shortage = result # tupple

        print(f"--- MATCH RESULTS FOR {args.crop.capitalize()} ---")
        print(f"Oversupply: {BOLD}{Oversupply['lgu'] + RESET} ({RED}{Oversupply['priority']}{RESET})")
        print(f"Shortage: {BOLD}{Shortage['lgu'] + RESET} ({RED}{Shortage['priority']}{RESET})")

        print(f"\nRecommendation: ")
        print(f"Transfer {args.crop.capitalize()} from"
              f" {GREEN}{Oversupply['lgu']}{RESET} -> {RED}{Shortage['lgu']}{RESET}")


        
    #list of entries 
    if args.list:
        
        monitor.show_pq()
        
    #gets most crit lgu
    if args.cget:        
        
        most = monitor.get_most_critical_LGU()
        if most is None:
            print("No LGUs in queue. Add Some?")
        else:
            print(f"Most critical LGU: {RED + BOLD + most + RESET}")

    if args.flush:
        print("Reseting...")
        monitor.flush_db()


if __name__ == "__main__":
    main()