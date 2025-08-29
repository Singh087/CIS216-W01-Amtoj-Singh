"""
Assignment 2 – Methods
CIS 216 – Amtoj Singh

This module extends the Session 1 BMI script into an object-oriented design
that focuses on METHODS. It supports both metric and imperial inputs and
demonstrates clean, PEP 8–compliant structure with docstrings and type hints.

External references used (for general BMI formula and adult categories):
- Wikiversity Lesson 2 (Methods): https://en.wikiversity.org/wiki/Object-Oriented_Programming/Methods
- CDC – Adult BMI information: https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
"""

from __future__ import annotations


class BMICalculator:
    """
    A calculator for Body Mass Index (BMI) with helper methods for
    validation, calculation, and categorization.

    Attributes:
        units (str): "metric" (kg, meters) or "imperial" (lb, inches)
    """

    VALID_UNITS = ("metric", "imperial")

    def __init__(self, units: str = "metric") -> None:
        """
        Initialize the BMI calculator with a unit system.

        Args:
            units: Either "metric" or "imperial".
        """
        units = units.lower().strip()
        if units not in self.VALID_UNITS:
            raise ValueError(f"Unsupported units '{units}'. Use 'metric' or 'imperial'.")
        self.units = units

    # -----------------------
    # Public API (Methods)
    # -----------------------

    def calculate_bmi(self, weight: float, height: float) -> float:
        """
        Calculate BMI based on the configured units.

        Args:
            weight: Weight in kilograms (metric) or pounds (imperial).
            height: Height in meters (metric) or inches (imperial).

        Returns:
            BMI as a float rounded to one decimal place.

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(weight, height)

        if self.units == "metric":
            bmi = self._bmi_metric(weight_kg=weight, height_m=height)
        else:
            bmi = self._bmi_imperial(weight_lb=weight, height_in=height)

        return round(bmi, 1)

    def get_category(self, bmi: float) -> str:
        """
        Categorize an adult BMI value using common thresholds.

        Args:
            bmi: A BMI value.

        Returns:
            A category string.
        """
        if bmi < 18.5:
            return "Underweight"
        if bmi < 25:
            return "Normal weight"
        if bmi < 30:
            return "Overweight"
        return "Obesity"

    def format_report(self, weight: float, height: float) -> str:
        """
        Produce a human-readable multi-line result string.

        Args:
            weight: Weight in configured units.
            height: Height in configured units.

        Returns:
            A concise report combining inputs, BMI, and category.
        """
        bmi = self.calculate_bmi(weight, height)
        category = self.get_category(bmi)

        unit_label_w, unit_label_h = ("kg", "m") if self.units == "metric" else ("lb", "in")
        return (
            f"Units     : {self.units}\n"
            f"Weight    : {weight} {unit_label_w}\n"
            f"Height    : {height} {unit_label_h}\n"
            f"BMI       : {bmi}\n"
            f"Category  : {category}"
        )

    # -----------------------
    # Internal Helpers
    # -----------------------

    def _validate_inputs(self, weight: float, height: float) -> None:
        """
        Validate inputs for positive, realistic values.
        """
        if weight is None or height is None:
            raise ValueError("Weight and height are required.")

        if not self._is_positive(weight) or not self._is_positive(height):
            raise ValueError("Weight and height must be positive numbers.")

        # Simple sanity checks to help catch input mistakes
        if self.units == "metric":
            # Rough human bounds (not strict medical validation)
            if not (1.0 <= height <= 2.7):
                raise ValueError("Metric height should be in meters, e.g., 1.75.")
            if not (20 <= weight <= 400):
                raise ValueError("Metric weight should be in kg, e.g., 70.")
        else:
            if not (36 <= height <= 110):
                raise ValueError("Imperial height should be in inches, e.g., 69.")
            if not (44 <= weight <= 880):
                raise ValueError("Imperial weight should be in pounds, e.g., 154.")

    @staticmethod
    def _is_positive(value: float) -> bool:
        return isinstance(value, (int, float)) and value > 0

    @staticmethod
    def _bmi_metric(weight_kg: float, height_m: float) -> float:
        """
        BMI (metric) = kg / m^2
        """
        return weight_kg / (height_m ** 2)

    @staticmethod
    def _bmi_imperial(weight_lb: float, height_in: float) -> float:
        """
        BMI (imperial) = 703 * lb / in^2
        """
        return 703 * weight_lb / (height_in ** 2)


def _prompt_units() -> str:
    """
    Ask the user for a unit system until a valid choice is provided.
    """
    while True:
        choice = input("Choose units: [M]etric (kg/m) or [I]mperial (lb/in): ").strip().lower()
        if choice in ("m", "metric"):
            return "metric"
        if choice in ("i", "imperial"):
            return "imperial"
        print("Please enter 'M' for metric or 'I' for imperial.")


def _prompt_float(prompt: str) -> float:
    """
    Prompt for a floating-point number with basic error handling.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            return value
        except ValueError:
            print("Please enter a valid number (e.g., 70 or 1.75).")


def main() -> None:
    """
    Interactive CLI entry point.
    """
    print("=== BMI Calculator (Assignment 2: Methods) ===")
    units = _prompt_units()
    calc = BMICalculator(units=units)

    if units == "metric":
        weight = _prompt_float("Enter weight (kg): ")
        height = _prompt_float("Enter height (m): ")
    else:
        weight = _prompt_float("Enter weight (lb): ")
        height = _prompt_float("Enter height (in): ")

    try:
        report = calc.format_report(weight, height)
        print("\n" + report)
    except ValueError as exc:
        print(f"\nInput error: {exc}")


if __name__ == "__main__":
    main()
