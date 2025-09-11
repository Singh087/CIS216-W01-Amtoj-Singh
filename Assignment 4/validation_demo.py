"""
CIS 216 – Assignment 4 (Validation)
Author: Amtoj Singh

One-file demo that validates a small list of “user signup” records and
keeps going even when some are bad. Prints GOOD vs BAD with reasons.

Non-Wikiversity refs (syntax only):
- Python try/except: https://docs.python.org/3/tutorial/errors.html
- datetime.date: https://docs.python.org/3/library/datetime.html#datetime.date
"""

from datetime import date
import re

# small allowed set for a cross-reference check
ALLOWED_US_STATES = {"IL", "WI", "IN", "MI", "IA", "MN", "MO", "OH"}

# basic pattern (kept simple on purpose)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_record(rec):
    """
    Minimal, readable checks. Raises ValueError with a short, human message.

    Validations shown:
      - Data type:       age=int, balance=float
      - Range/constraint: age in 0..110, balance >= 0, password length >= 8
      - Structured:      email matches a simple pattern
      - Code/x-ref:      if country == 'US', state must be in our allowed set
      - Consistency:     start_date <= end_date
    """
    # pull + trim
    name = str(rec.get("name", "")).strip()
    email = str(rec.get("email", "")).strip()
    age = rec.get("age", None)
    balance = rec.get("balance", None)
    password = str(rec.get("password", ""))
    country = str(rec.get("country", "")).upper()
    state = str(rec.get("state", "")).upper()
    start_date = rec.get("start_date", None)
    end_date = rec.get("end_date", None)

    if not name:
        raise ValueError("name is required")

    # structured / pattern
    if not EMAIL_RE.match(email):
        raise ValueError("email looks invalid")

    # data type + range/constraint (age)
    if not isinstance(age, int):
        raise ValueError("age must be an integer")
    if not (0 <= age <= 110):
        raise ValueError("age must be between 0 and 110")

    # data type + range/constraint (balance)
    try:
        bal = float(balance)
    except Exception:
        raise ValueError("balance must be a number")
    if bal < 0:
        raise ValueError("balance cannot be negative")

    # range/constraint (password length)
    if len(password) < 8:
        raise ValueError("password must be at least 8 characters")

    # code/x-ref + nested if example
    if country == "US":
        if state not in ALLOWED_US_STATES:
            raise ValueError("state must be a valid 2-letter code for US in our list")

    # consistency: dates present and ordered
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise ValueError("start_date and end_date must be date objects")
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date")

    # return a normalized dict
    return {
        "name": name,
        "email": email,
        "age": age,
        "balance": round(bal, 2),
        "country": country,
        "state": state if country == "US" else "",
        "start_date": start_date,
        "end_date": end_date,
    }


def run_demo():
    # realistic sample data (first one uses your Harper email)
    records = [
        {
            "name": "Amtoj Singh",
            "email": "sa48190@mail.harpercollege.edu",
            "age": 24,
            "balance": 125.75,
            "password": "StrongPass1",
            "country": "US",
            "state": "IL",
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        {
            "name": "Short Password",
            "email": "ok@example.com",
            "age": 20,
            "balance": 10,
            "password": "short",  # length < 8
            "country": "US",
            "state": "IL",
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        {
            "name": "Bad Email",
            "email": "not-an-email",
            "age": 19,
            "balance": 0,
            "password": "abcdefgh",
            "country": "US",
            "state": "WI",
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        {
            "name": "Too Old",
            "email": "too.old@example.com",
            "age": 200,  # range fail
            "balance": 10,
            "password": "abcdefgh",
            "country": "US",
            "state": "IL",
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        {
            "name": "Wrong State",
            "email": "ws@example.com",
            "age": 22,
            "balance": 5.5,
            "password": "abcdefgh",
            "country": "US",
            "state": "CA",  # not in our small set
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 12, 15),
        },
        {
            "name": "Negative Balance / Bad Dates",
            "email": "nb@example.com",
            "age": 30,
            "balance": -3.14,  # constraint fail
            "password": "abcdefgh",
            "country": "CA",
            "state": "",
            "start_date": date(2025, 9, 10),
            "end_date": date(2025, 9, 9),  # consistency fail
        },
    ]

    good = []
    bad = []

    for idx, rec in enumerate(records, start=1):
        try:
            clean = validate_record(rec)
            good.append(clean)
        except ValueError as e:
            # catch and continue
            who = rec.get("name", f"record#{idx}")
            bad.append((who, str(e)))
        except Exception as e:
            # catch-all (unexpected)
            who = rec.get("name", f"record#{idx}")
            bad.append((who, f"unexpected error: {e!r}"))

    print("=== GOOD RECORDS ===")
    for g in good:
        print(
            f"- {g['name']} | {g['email']} | age={g['age']} | "
            f"{g['country']} {g['state']} | balance=${g['balance']} | "
            f"{g['start_date']} → {g['end_date']}"
        )

    print("\n=== BAD RECORDS (reason) ===")
    for who, reason in bad:
        print(f"- {who}: {reason}")

    print(f"\nSummary: {len(good)} good, {len(bad)} bad, total {len(good)+len(bad)}")


if __name__ == "__main__":
    run_demo()
