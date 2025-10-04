"""
Subclass: Car(Vehicle)
Unique: seats (int)
Overrides: drive(miles)
"""

from vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, make: str, model: str, year: int, seats: int = 5) -> None:
        super().__init__(make, model, year)
        self.seats = seats

    @property
    def seats(self) -> int:
        return self._seats

    @seats.setter
    def seats(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("seats must be a positive integer")
        self._seats = value

    def drive(self, miles: float) -> str:
        return f"Car {self.description()} cruises {miles}mi with {self.seats} seats."

    def __str__(self) -> str:
        return f"Car: {self.description()} ({self.seats} seats)"
