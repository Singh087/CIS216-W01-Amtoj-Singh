"""
Unit tests for Assignment 7 – Polymorphism (Vehicles)
Run:
    python -m unittest discover -s "Assignment 7" -p "test_*.py" -v
"""

import unittest
from vehicle import Vehicle
from car import Car
from truck import Truck
from motorcycle import Motorcycle


class TestVehicleBase(unittest.TestCase):
    def test_description_and_validation(self):
        v = Vehicle("Honda", "Civic", 2018)
        self.assertEqual(v.description(), "2018 Honda Civic")
        with self.assertRaises(NotImplementedError):
            v.drive(10)

        with self.assertRaises(ValueError):
            Vehicle("", "Model", 2018)
        with self.assertRaises(ValueError):
            Vehicle("Make", "", 2018)
        with self.assertRaises(ValueError):
            Vehicle("Make", "Model", 1700)  # too early


class TestCar(unittest.TestCase):
    def test_car_drive_and_str(self):
        c = Car("Toyota", "Camry", 2021, seats=5)
        self.assertIn("cruises", c.drive(5))
        self.assertIn("seats", str(c))
        with self.assertRaises(ValueError):
            Car("Toyota", "Camry", 2021, seats=0)


class TestTruck(unittest.TestCase):
    def test_truck_drive_and_str(self):
        t = Truck("Ford", "F-150", 2020, payload_capacity_lbs=2500)
        self.assertIn("hauls", t.drive(7.2))
        self.assertIn("payload", str(t))
        with self.assertRaises(ValueError):
            Truck("Ford", "F-150", 2020, payload_capacity_lbs=-1)


class TestMotorcycle(unittest.TestCase):
    def test_motorcycle_drive_and_str(self):
        m = Motorcycle("Honda", "CBR500R", 2022, cc=471)
        self.assertIn("zips", m.drive(3.3))
        self.assertIn("cc", str(m))
        with self.assertRaises(ValueError):
            Motorcycle("Honda", "CBR500R", 2022, cc=0)


class TestPolymorphism(unittest.TestCase):
    def test_loop_polymorphism(self):
        fleet = [
            Car("Toyota", "Camry", 2021, seats=5),
            Truck("Ford", "F-150", 2020, payload_capacity_lbs=2500),
            Motorcycle("Honda", "CBR500R", 2022, cc=471),
        ]
        # single interface call; different behaviors
        outputs = [v.drive(10) for v in fleet]
        self.assertTrue(any("cruises" in s for s in outputs))
        self.assertTrue(any("hauls" in s for s in outputs))
        self.assertTrue(any("zips" in s for s in outputs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
