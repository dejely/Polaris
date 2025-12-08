from supply_monitor import SupplyMonitor 
import argparse as ap
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'



def main():
    monitor = SupplyMonitor(use_sorted=True)
    parser = ap.ArgumentParser(description="POLARIS: Logistic System")

    parser.add_argument('--add', help="Add a new LGU", action="store_true")
    parser.add_argument('--cget', help="Get the most critical LGU", action="store_true")
    parser.add_argument('--list', help="List all the LGUs and Status", action="store_true")

    #args for adding a LGU
    parser.add_argument('--lgu', help="Add LGU name", type = str)
    parser.add_argument('--curr', help="Add the current supply in the LGU", type = int)
    parser.add_argument('--ideal', help="Add the ideal supply in the LGU", type = int)

    args = parser.parse_args()

    if args.add:
        if not (args.lgu and (args.curr is not None) and (args.ideal is not None)):
            print("Error: Please Complete the format -> --lgu [lgu] --curr_supply[int] --ideal_supply[int]")
            return
        
    if args.list:
        monitor.show_pq()

    if args.cget:        
        most = monitor.get_most_critical_LGU()
        if most is None:
            print("No LGUs in queue. Add Some?")
        else:
            print(f"Most critical LGU: {RED + BOLD + monitor.get_most_critical_LGU() + RESET}")

    
    monitor.supply_checker(args.lgu, curr_supply=args.curr, ideal_supply=args.ideal)
    print(f"Added LGU: {args.lgu} (curr={args.curr}, ideal={args.ideal})")
        
    


    monitor.supply_checker("Nueva Vizcaya", curr_supply=500, ideal_supply=100)
    monitor.supply_checker("Cebu City", curr_supply=50, ideal_supply=200)
    monitor.supply_checker("Benguet", curr_supply=300, ideal_supply=250)

    #prints the current standing of priority list
    monitor.show_pq()

    print(f"Most critical LGU: {RED + BOLD + monitor.get_most_critical_LGU() + RESET}")

if __name__ == "__main__":
    main()