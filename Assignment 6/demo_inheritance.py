"""
Demo for Assignment 6 – Inheritance (Employees)
Shows polymorphism and unique behaviors.
"""

from manager import Manager
from sales import SalesEmployee
from hourly import HourlyEmployee

def main():
    m = Manager("Alice Manager", "alice@college.edu", 101, 78000, 8)
    s = SalesEmployee("Bob Sales", "bob@college.edu", 102, 500, 0.15)
    h = HourlyEmployee("Cara Hourly", "cara@college.edu", 103, 22.5)

    roster = [m, s, h]
    print("=== Staff Directory ===")
    for person in roster:
        print("-", person, "| Contact:", person.contact_info())

    print("\n=== Pay Examples ===")
    print("Manager biweekly:", m.compute_pay(26))
    print("Sales (2400 sales):", s.compute_pay(2400))
    print("Hourly (43 hrs):", h.compute_pay(43))

    print("\nGiving Manager a 5% raise...")
    m.give_raise(5)
    print(m)

if __name__ == "__main__":
    main()
