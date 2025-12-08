from supply_monitor import SupplyMonitor 



def main():






monitor = SupplyMonitor(use_sorted=True)

monitor.supply_checker("Nueva Vizcaya", curr_supply=500, ideal_supply=100)
monitor.supply_checker("Cebu City", curr_supply=50, ideal_supply=200)
monitor.supply_checker("Benguet", curr_supply=300, ideal_supply=250)

print("Most critical LGU:")
print(monitor.get_most_critical_LGU())