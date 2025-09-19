"""
CIS 216 – Assignment 5 (Unit Testing)
Author: Amtoj Singh

Purpose:
  Small, testable BMI utilities and a tiny demo so graders can run the file.
  Functions are intentionally small and explicit for clear unit tests.

Non-Wikiversity references:
  - unittest docs: https://docs.python.org/3/library/unittest.html
  - Exceptions: https://docs.python.org/3/tutorial/errors.html
"""

from __future__ import annotations
from typing import Iterable, List


def calculate_bmi_metric(weight_kg: float, height_m: float) -> float:
    """
    Calculate BMI using metric units and return value rounded to 1 decimal.

    Raises ValueError for missing/non-numeric/nonpositive/unrealistic inputs.
    """
    try:
        w = float(weight_kg)
        h = float(height_m)
    except (TypeError, ValueError):
        raise ValueError("weight_kg and height_m must be numeric")

    if w <= 0 or h <= 0:
        raise ValueError("weight and height must be > 0")
    # sanity bounds to catch obvious mistakes (not medical rules)
    if w > 500 or not (0.4 <= h <= 3.0):
        raise ValueError("unrealistic weight/height provided")

    bmi_raw = w / (h ** 2)
    return round(bmi_raw, 1)


def bmi_category(bmi: float) -> str:
    """
    Return an adult BMI category for a numeric BMI value.

    Raises ValueError if bmi is not numeric.
    """
    try:
        v = float(bmi)
    except (TypeError, ValueError):
        raise ValueError("bmi must be a number")

    if v < 18.5:
        return "Underweight"
    if v < 25:
        return "Normal"
    if v < 30:
        return "Overweight"
    return "Obesity"


def average_bmi(values: Iterable[float]) -> float:
    """
    Compute the average of BMI numbers (non-empty iterable) rounded to 0.1.
    Raises ValueError if values is empty or contains non-numeric items.
    """
    if values is None:
        raise ValueError("values is required")

    nums: List[float] = []
    for item in values:
        try:
            nums.append(float(item))
        except (TypeError, ValueError):
            raise ValueError("all items in values must be numeric")

    if len(nums) == 0:
        raise ValueError("values must be non-empty")

    avg = sum(nums) / len(nums)
    return round(avg, 1)


def safe_divide(numerator: float, denominator: float) -> float:
    """
    Simple helper showing exception behavior: raises ZeroDivisionError on den == 0.
    """
    try:
        num = float(numerator)
        den = float(denominator)
    except (TypeError, ValueError):
        raise ValueError("numerator and denominator must be numbers")
    if den == 0:
        raise ZeroDivisionError("denominator cannot be zero")
    return num / den


def _demo() -> None:
    """Small demo output so graders can run the module directly."""
    print("CIS 216 — BMI tools demo")
    try:
        print(" - BMI for 82 kg, 1.81 m ->", calculate_bmi_metric(82, 1.81))
        print(" - Category for BMI 25.0 ->", bmi_category(25.0))
        print(" - Average BMI for [22, 24, 26] ->", average_bmi([22, 24, 26]))
        print(" - safe_divide 10/2 ->", safe_divide(10, 2))
    except Exception as e:
        print("Demo error:", e)


if __name__ == "__main__":
    _demo()
