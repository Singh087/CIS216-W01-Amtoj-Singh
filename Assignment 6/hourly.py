"""
Child class: HourlyEmployee(Employee)
Unique: hourly_rate
Overrides compute_pay() to handle overtime
"""

from employee import Employee

class HourlyEmployee(Employee):
    def __init__(self, name, email, employee_id, hourly_rate):
        super().__init__(name, email, employee_id)
        self.hourly_rate = hourly_rate

    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        v = float(value)
        if v <= 0:
            raise ValueError("Hourly rate must be > 0")
        self._hourly_rate = round(v, 2)

    def compute_pay(self, hours_worked: float) -> float:
        h = float(hours_worked)
        if h < 0:
            raise ValueError("Hours worked cannot be negative")
        regular = min(h, 40)
        overtime = max(h - 40, 0)
        return round(regular * self.hourly_rate + overtime * self.hourly_rate * 1.5, 2)

    def __str__(self):
        return f"Hourly #{self.employee_id}: {self.name}, ${self.hourly_rate}/hr"


if __name__ == "__main__":
    import unittest
    from test_employees import TestHourly  # noqa
    unittest.main(verbosity=2)
