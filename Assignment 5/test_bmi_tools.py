"""
Unit tests for Assignment 5 — bmi_tools.py

Run:
    python -m unittest discover -s "Assignment 5" -v
"""

import unittest
from bmi_tools import (
    calculate_bmi_metric,
    bmi_category,
    average_bmi,
    safe_divide,
)


class TestCalculateBMIMetric(unittest.TestCase):
    def test_basic_calculation(self):
        self.assertEqual(calculate_bmi_metric(82, 1.81), 25.0)

    def test_rounding(self):
        self.assertEqual(calculate_bmi_metric(70, 1.75), 22.9)

    def test_invalid_types(self):
        with self.assertRaises(ValueError):
            calculate_bmi_metric("not-a-number", 1.8)
        with self.assertRaises(ValueError):
            calculate_bmi_metric(70, "nope")

    def test_nonpositive_values(self):
        with self.assertRaises(ValueError):
            calculate_bmi_metric(0, 1.8)
        with self.assertRaises(ValueError):
            calculate_bmi_metric(70, 0)

    def test_unrealistic_values(self):
        with self.assertRaises(ValueError):
            calculate_bmi_metric(600, 1.8)
        with self.assertRaises(ValueError):
            calculate_bmi_metric(70, 0.1)
        with self.assertRaises(ValueError):
            calculate_bmi_metric(70, 5.0)


class TestBMICategory(unittest.TestCase):
    def test_boundaries_and_labels(self):
        self.assertEqual(bmi_category(18.4), "Underweight")
        self.assertEqual(bmi_category(18.5), "Normal")
        self.assertEqual(bmi_category(24.9), "Normal")
        self.assertEqual(bmi_category(25.0), "Overweight")
        self.assertEqual(bmi_category(29.9), "Overweight")
        self.assertEqual(bmi_category(30.0), "Obesity")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            bmi_category("abc")


class TestAverageBMI(unittest.TestCase):
    def test_average_simple(self):
        self.assertEqual(average_bmi([22.0, 24.0, 26.0]), 24.0)

    def test_average_with_strings_numbers(self):
        self.assertEqual(average_bmi(["22.0", 24, 26.0]), 24.0)

    def test_empty_list_error(self):
        with self.assertRaises(ValueError):
            average_bmi([])

    def test_non_numeric_item_error(self):
        with self.assertRaises(ValueError):
            average_bmi([22, "x", 24])


class TestSafeDivide(unittest.TestCase):
    def test_division_ok(self):
        self.assertAlmostEqual(safe_divide(10, 2), 5.0)

    def test_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            safe_divide(1, 0)

    def test_invalid_types(self):
        with self.assertRaises(ValueError):
            safe_divide("a", 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
