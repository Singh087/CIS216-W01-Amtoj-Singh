"""
Assignment 3 – Conditions, Data Validations, and Exception Handling
CIS 216 – Amtoj Singh

This script demonstrates:
  (#1) Multiple validation checks:
       - Data type validation
       - Range/constraint validation
       - Code & cross-reference validation
       - Structured (pattern) validation
       - Consistency validation
  (#2) Python exception handling with try/except
  (#3) A nested if statement

Behavior:
- Processes a batch of enrollment-like records.
- Validates each field; separates GOOD vs BAD data.
- Continues processing even when some records are invalid.
- Prints a summary report at the end.

Note: Email regex is intentionally simple for demonstration.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Dict, List, Tuple, Any


ALLOWED_STATES = {
    "IL", "WI", "IN", "MI", "IA", "MN", "MO", "OH"  # small Midwest sample
}

COURSE_CATALOG = {
    "CIS216": "Applied Object-Oriented Programming",
    "CIS143": "Introduction to Databases",
    "CIS101": "Intro to Computer Information Systems",
}


class ValidationError(Exception):
    """Custom exception to represent validation failures."""


class RecordValidator:
    """
    Encapsulates validation logic.
    Demonstrates methods, conditions, and exception handling.
    """

    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def validate(self, rec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single record and return a normalized version.

        Expected keys:
          - name: str (non-empty)
          - email: str (simple email structure)
          - age: int (0..100)
          - country: str (e.g., "US" or something else)
          - state: str (2-letter if country == "US")
          - course_code: str (must exist in COURSE_CATALOG)
          - gpa_numerator: float
          - gpa_denominator: float (non-zero)
          - start_date: date
          - end_date: date  (end_date >= start_date)
        """
        normalized = {}

        # --- Data type + basic presence checks (DATA TYPE VALIDATION) (#1)
        try:
            name = str(rec.get("name", "")).strip()
            email = str(rec.get("email", "")).strip()
            age = rec.get("age")
            country = str(rec.get("country", "")).strip().upper()
            state = str(rec.get("state", "")).strip().upper()
            course_code = str(rec.get("course_code", "")).strip().upper()
            gpa_num = float(rec.get("gpa_numerator"))
            gpa_den = float(rec.get("gpa_denominator"))
            start_date_val = rec.get("start_date")
            end_date_val = rec.get("end_date")
        except (TypeError, ValueError) as exc:
            # (#2) Exception handling for type conversion problems
            raise ValidationError(f"Type conversion failed: {exc}") from exc

        if not name:
            raise ValidationError("Name is required.")

        # --- Structured validation: email looks like an email (#1)
        if not self.EMAIL_REGEX.match(email):
            raise ValidationError("Email format is invalid.")

        # --- Range/constraint validation: age 0..100, GPA 0..4 after division (#1)
        if not isinstance(age, int):
            raise ValidationError("Age must be an integer.")
        if not (0 <= age <= 100):
            raise ValidationError("Age must be between 0 and 100.")

        # --- Code & cross-reference validation: course exists (#1)
        if course_code not in COURSE_CATALOG:
            raise ValidationError(f"Unknown course_code '{course_code}'.")

        # --- Nested if example (#3):
        # If country is US, then a valid 2-letter state must be provided from ALLOWED_STATES
        if country == "US":
            if state not in ALLOWED_STATES:
                raise ValidationError(
                    f"For US addresses, state must be one of: {sorted(ALLOWED_STATES)}"
                )
        else:
            # For non-US, we don't require state; empty is acceptable
            state = ""

        # --- Consistency validation: start_date <= end_date (#1)
        if not isinstance(start_date_val, date) or not isinstance(end_date_val, date):
            raise ValidationError("start_date and end_date must be date objects.")
        if end_date_val < start_date_val:
            raise ValidationError("end_date must be on or after start_date.")

        # --- Exception example: potential ZeroDivisionError when computing GPA (#2)
        try:
            gpa = gpa_num / gpa_den
        except ZeroDivisionError as exc:
            raise ValidationError("GPA denominator cannot be zero.") from exc

        # Add a reasonable constraint for GPA
        if not (0.0 <= gpa <= 4.0):
            raise ValidationError("Computed GPA must be between 0.0 and 4.0.")

        # If everything passes, return normalized record
        normalized.update(
            {
                "name": name,
                "email": email,
                "age": age,
                "country": country,
                "state": state,
                "course_code": course_code,
                "course_title": COURSE_CATALOG[course_code],
                "gpa": round(gpa, 2),
                "start_date": start_date_val,
                "end_date": end_date_val,
            }
        )
        return normalized


def process_records(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Tuple[Dict[str, Any], str]]]:
    """
    Validate a list of records, return (good_records, bad_records_with_error_message).

    Demonstrates continuing after bad data is encountered.
    """
    validator = RecordValidator()
    good, bad = [], []

    for idx, rec in enumerate(records, start=1):
        try:
            clean = validator.validate(rec)
            good.append(clean)
        except ValidationError as ve:
            # (#2) Exception handling: capture + continue
            bad.append((rec, f"Record #{idx} failed: {ve}"))
        except Exception as e:
            # Catch-all to mimic robust pipelines; typically you would log this.
            bad.append((rec, f"Record #{idx} unexpected error: {e!r}"))

    return good, bad


def demo() -> None:
    """
    Run a small demonstration batch that includes a mix of valid and invalid records.
    """
    sample_records = [
        # Valid US record
        {
            "name": "Amtoj Singh",
            "email": "amtoj.singh@example.com",
            "age": 24,
            "country": "US",
            "state": "IL",
            "course_code": "CIS216",
            "gpa_numerator": 12.0,
            "gpa_denominator": 3.0,
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        # Invalid: email structure
        {
            "name": "Bad Email",
            "email": "not-an-email",
            "age": 20,
            "country": "US",
            "state": "WI",
            "course_code": "CIS143",
            "gpa_numerator": 10.0,
            "gpa_denominator": 2.5,
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        # Invalid: age out of range
        {
            "name": "Too Old",
            "email": "too.old@example.com",
            "age": 200,
            "country": "US",
            "state": "IL",
            "course_code": "CIS101",
            "gpa_numerator": 8.0,
            "gpa_denominator": 2.0,
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        # Invalid: US but bad state code
        {
            "name": "Wrong State",
            "email": "ws@example.com",
            "age": 25,
            "country": "US",
            "state": "CA",  # not in our small allowed set
            "course_code": "CIS216",
            "gpa_numerator": 9.0,
            "gpa_denominator": 3.0,
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        # Invalid: course not in catalog
        {
            "name": "Unknown Course",
            "email": "uc@example.com",
            "age": 22,
            "country": "US",
            "state": "IL",
            "course_code": "MATH999",
            "gpa_numerator": 12.0,
            "gpa_denominator": 3.0,
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        # Invalid: GPA denominator zero (exception path)
        {
            "name": "Zero Den",
            "email": "zd@example.com",
            "age": 21,
            "country": "US",
            "state": "IN",
            "course_code": "CIS143",
            "gpa_numerator": 10.0,
            "gpa_denominator": 0.0,  # triggers ZeroDivisionError -> ValidationError
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        # Non-US record (state optional), but inconsistent dates (end < start)
        {
            "name": "Intl Student",
            "email": "intl.student@example.org",
            "age": 23,
            "country": "CA",
            "state": "",
            "course_code": "CIS216",
            "gpa_numerator": 14.0,
            "gpa_denominator": 4.0,
            "start_date": date(2025, 12, 20),
            "end_date": date(2025, 9, 1),
        },
    ]

    good, bad = process_records(sample_records)

    print("=== GOOD RECORDS ===")
    for g in good:
        print(
            f"- {g['name']} | {g['email']} | {g['course_code']} ({g['course_title']}) | "
            f"GPA={g['gpa']} | {g['country']} {g['state']} | {g['start_date']} → {g['end_date']}"
        )

    print("\n=== BAD RECORDS (with reasons) ===")
    for rec, err in bad:
        who = rec.get("name", "<unknown>")
        print(f"- {who}: {err}")

    print(f"\nSummary: {len(good)} good, {len(bad)} bad, total {len(good) + len(bad)}.")


if __name__ == "__main__":
    demo()
