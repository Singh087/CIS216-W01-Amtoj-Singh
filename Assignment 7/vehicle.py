"""
CIS 216 – Assignment 7 (Polymorphism)
Author: Amtoj Singh

Base class: Vehicle
- Shared properties (make, model, year) with light validation
- Shared method: description()
- Polymorphic method: drive(...)  -> intended to be overridden by subclasses

Reference (non-Wikiversity):
- Python classes & inheritance: https://docs.python.org/3/tutorial/classes.html
"""

class Vehicle:
    def __init__(self, make: str, model: str, year: int) -> None:
        self.make = make
        self.model = model
        self.year = year

    # --- properties (kept simple on purpose) ---
    @property
    def make(self) -> str:
        return self._make

    @make.setter
    def make(self, value: str) -> None:
        v = (value or "").strip()
        if not v:
            raise ValueError("make cannot be empty")
        self._make = v.title()

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        v = (value or "").strip()
        if not v:
            raise ValueError("model cannot be empty")
        self._model = v.title()

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        # first gas/petrol car was ~1886; keep a loose future cap
        if not isinstance(value, int) or not (1886 <= value <= 2100):
            raise ValueError("year must be an int in [1886, 2100]")
        self._year = value

    # --- shared behavior ---
    def description(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    def drive(self, miles: float) -> str:
        """
        Polymorphic interface: subclasses override this to provide
        class-specific driving behavior. Returning a string makes it easy to test.
        """
        raise NotImplementedError("Subclasses must implement drive(miles).")

    def __str__(self) -> str:
        return self.description()


# Auto-run tests if this file is executed directly (handy for graders)
if __name__ == "__main__":
    import unittest
    from test_vehicles import TestVehicleBase  # noqa: F401
    unittest.main(verbosity=2)
