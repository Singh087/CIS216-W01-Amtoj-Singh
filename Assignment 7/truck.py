"""
Subclass: Truck(Vehicle)
Unique: payload_capacity (in pounds)
Overrides: drive(miles)
"""

from vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, make: str, model: str, year: int, payload_capacity_lbs: int) -> None:
        super().__init__(make, model, year)
        self.payload_capacity_lbs = payload_capacity_lbs

    @property
    def payload_capacity_lbs(self) -> int:
        return self._payload_capacity_lbs

    @payload_capacity_lbs.setter
    def payload_capacity_lbs(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("payload_capacity_lbs must be a positive integer")
        self._payload_capacity_lbs = value

    def drive(self, miles: float) -> str:
        return f"Truck {self.description()} hauls for {miles}mi (payload {self.payload_capacity_lbs} lbs)."

    def __str__(self) -> str:
        return f"Truck: {self.description()} ({self.payload_capacity_lbs} lbs payload)"
