"""
Child class: Manager(Employee)
Unique: annual_salary, bonus_percent
Adds give_raise() and compute_pay()

TODO: maybe add monthly/weekly pay calendars in future
"""

from employee import Employee

class Manager(Employee):
    def __init__(self, name, email, employee_id, annual_salary, bonus_percent=0.0):
        super().__init__(name, email, employee_id)
        self.annual_salary = annual_salary
        self.bonus_percent = bonus_percent

    @property
    def annual_salary(self) -> float:
        return self._annual_salary

    @annual_salary.setter
    def annual_salary(self, value: float) -> None:
        v = float(value)
        if v < 0:
            raise ValueError("Annual salary cannot be negative")
        self._annual_salary = round(v, 2)

    @property
    def bonus_percent(self) -> float:
        return self._bonus_percent

    @bonus_percent.setter
    def bonus_percent(self, value: float) -> None:
        v = float(value)
        if v < 0:
            raise ValueError("Bonus percent must be >= 0")
        self._bonus_percent = v

    def give_raise(self, percent: float) -> None:
        self.annual_salary = self.annual_salary * (1 + percent / 100.0)

    def compute_pay(self, periods: int = 26) -> float:
        """Biweekly by default (26 periods)."""
        base = self.annual_salary / periods
        return round(base * (1 + self.bonus_percent / 100.0), 2)

    def __str__(self):
        return f"Manager #{self.employee_id}: {self.name}, ${self.annual_salary}/yr"


if __name__ == "__main__":
    import unittest
    from test_employees import TestManager  # noqa
    unittest.main(verbosity=2)
