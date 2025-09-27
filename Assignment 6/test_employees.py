"""
Unit tests for Assignment 6 – Employees
Run:
    python -m unittest discover -s "Assignment 6" -p "test_*.py" -v
"""

import unittest
from employee import Employee
from manager import Manager
from sales import SalesEmployee
from hourly import HourlyEmployee

class TestEmployeeBase(unittest.TestCase):
    def test_contact_info(self):
        e = Employee("Amtoj Singh", "sa48190@mail.harpercollege.edu", 1001)
        self.assertIn("Amtoj Singh", e.contact_info())
    def test_compute_pay_abstract(self):
        e = Employee("Test", "t@e.com", 2)
        with self.assertRaises(NotImplementedError):
            e.compute_pay()

class TestManager(unittest.TestCase):
    def test_pay_and_raise(self):
        m = Manager("Boss", "boss@corp.com", 2001, 78000, 10)
        self.assertAlmostEqual(m.compute_pay(26), round(78000/26*1.10,2))
        m.give_raise(5)
        self.assertGreater(m.annual_salary, 78000)

class TestSales(unittest.TestCase):
    def test_commission_and_pay(self):
        s = SalesEmployee("Sam", "sam@sales.com", 3001, 500, 0.2)
        self.assertEqual(s.record_sales(1000), 200.0)
        self.assertEqual(s.compute_pay(1500), 500 + 300)

class TestHourly(unittest.TestCase):
    def test_regular_and_overtime(self):
        h = HourlyEmployee("Hana", "hana@work.com", 4001, 20)
        self.assertEqual(h.compute_pay(38), 760)
        self.assertEqual(h.compute_pay(45), 40*20 + 5*30)

class TestPoly(unittest.TestCase):
    def test_polymorphic_print(self):
        staff = [
            Manager("Boss", "b@c.com", 1, 50000, 5),
            SalesEmployee("Sam", "s@c.com", 2, 400, 0.1),
            HourlyEmployee("Hana", "h@c.com", 3, 25)
        ]
        lines = [str(p) for p in staff]
        self.assertTrue(any("Manager" in line for line in lines))
        self.assertTrue(any("Sales" in line for line in lines))
        self.assertTrue(any("Hourly" in line for line in lines))

if __name__ == "__main__":
    unittest.main(verbosity=2)
