"""
CIS 216 – Assignment 6 (Inheritance)
Author: Amtoj Singh

Base class: Employee
Shared fields: name, email, employee_id
Shared methods: contact_info, __str__, compute_pay (abstract placeholder)

Reference:
- Python docs on classes & inheritance: https://docs.python.org/3/tutorial/classes.html
"""

class Employee:
    def __init__(self, name: str, email: str, employee_id: int) -> None:
        self.name = name
        self.email = email
        self.employee_id = employee_id

    # --- properties ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip().title()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        v = (value or "").strip()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Email must look like user@example.com")
        self._email = v

    @property
    def employee_id(self) -> int:
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Employee ID must be a positive integer")
        self._employee_id = value

    # --- shared methods ---
    def contact_info(self) -> str:
        return f"{self.name} <{self.email}>"

    def compute_pay(self, *args, **kwargs) -> float:
        """Abstract-ish: subclasses are expected to override this."""
        raise NotImplementedError("Subclasses must implement compute_pay().")

    def __str__(self) -> str:
        return f"Employee #{self.employee_id}: {self.name}"


# Run tests automatically when this file is executed
if __name__ == "__main__":
    import unittest
    from test_employees import TestEmployeeBase  # noqa
    unittest.main(verbosity=2)
