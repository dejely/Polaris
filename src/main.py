from supply_monitor import SupplyMonitor 
import argparse as ap


def main():
    parser = ap.ArgumentParser(description="POLARIS: Logistic System")

    parser.add_argument('--add', help="Add a new LGU", action="store_true")
    parser.add_argument('--cget', help="Get the most critical LGU", action="store_true")
    parser.add_argument('--list', help="List all the LGUs and Status", action="store_true")

    #args for adding a LGU

monitor = SupplyMonitor(use_sorted=True)

monitor.supply_checker("Nueva Vizcaya", curr_supply=500, ideal_supply=100)
monitor.supply_checker("Cebu City", curr_supply=50, ideal_supply=200)
monitor.supply_checker("Benguet", curr_supply=300, ideal_supply=250)

#prints the current standing of priority list
monitor.show_pq()

print("Most critical LGU:")
print(monitor.get_most_critical_LGU())