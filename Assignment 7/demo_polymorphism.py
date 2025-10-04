"""
Demo for Assignment 7 – Polymorphism
- Creates Car, Truck, Motorcycle (all derive from Vehicle)
- Loops vehicles as Vehicle references and calls drive() (polymorphism)
"""

from car import Car
from truck import Truck
from motorcycle import Motorcycle

def main() -> None:
    fleet = [
        Car("Toyota", "Camry", 2021, seats=5),
        Truck("Ford", "F-150", 2020, payload_capacity_lbs=2500),
        Motorcycle("Honda", "CBR500R", 2022, cc=471),
    ]

    print("=== Fleet directory ===")
    for v in fleet:
        print(" -", v)

    print("\n=== Polymorphic driving ===")
    for v in fleet:
        # each subclass implements drive() differently, but we call the same interface
        print(v.drive(12.5))

    # tiny validation showcase (caught error, keep demo moving)
    print("\n=== Validation example (caught) ===")
    try:
        Car("NoName", "", 2021, seats=0)
    except ValueError as e:
        print("Expected error:", e)

if __name__ == "__main__":
    main()
