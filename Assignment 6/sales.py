"""
Child class: SalesEmployee(Employee)
Unique: base_pay, commission_rate
Adds record_sales() and overrides compute_pay()
"""

from employee import Employee

class SalesEmployee(Employee):
    def __init__(self, name, email, employee_id, base_pay, commission_rate):
        super().__init__(name, email, employee_id)
        self.base_pay = base_pay
        self.commission_rate = commission_rate

    @property
    def base_pay(self) -> float:
        return self._base_pay

    @base_pay.setter
    def base_pay(self, value: float) -> None:
        v = float(value)
        if v < 0:
            raise ValueError("Base pay must be non-negative")
        self._base_pay = round(v, 2)

    @property
    def commission_rate(self) -> float:
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float) -> None:
        v = float(value)
        if not (0 <= v <= 1):
            raise ValueError("Commission rate must be between 0.0 and 1.0")
        self._commission_rate = v

    def record_sales(self, amount: float) -> float:
        a = float(amount)
        if a < 0:
            raise ValueError("Sales cannot be negative")
        return round(a * self.commission_rate, 2)

    def compute_pay(self, sales_amount: float) -> float:
        return round(self.base_pay + self.record_sales(sales_amount), 2)

    def __str__(self):
        return f"Sales #{self.employee_id}: {self.name}, base ${self.base_pay}, {self.commission_rate*100:.1f}% commission"


if __name__ == "__main__":
    import unittest
    from test_employees import TestSales  # noqa
    unittest.main(verbosity=2)
