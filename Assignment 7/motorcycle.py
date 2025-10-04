"""
Subclass: Motorcycle(Vehicle)
Unique: cc (engine displacement)
Overrides: drive(miles)
"""

from vehicle import Vehicle

class Motorcycle(Vehicle):
    def __init__(self, make: str, model: str, year: int, cc: int) -> None:
        super().__init__(make, model, year)
        self.cc = cc

    @property
    def cc(self) -> int:
        return self._cc

    @cc.setter
    def cc(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("cc must be a positive integer")
        self._cc = value

    def drive(self, miles: float) -> str:
        return f"Motorcycle {self.description()} zips {miles}mi ({self.cc}cc)."

    def __str__(self) -> str:
        return f"Motorcycle: {self.description()} ({self.cc}cc)"
