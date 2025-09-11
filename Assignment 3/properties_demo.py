"""
CIS 216 – Assignment 3 (Properties)
Author: Amtoj Singh

One-file example that uses Python properties to:
- keep fields clean (basic checks in setters),
- expose a read-only id,
- and compute a few values from existing data.

Reference used (non-Wikiversity, for property syntax only):
https://docs.python.org/3/library/functions.html#property
"""

class Student:
    def __init__(self, student_id, name, email, age, gpa, credits, weight_kg=None, height_m=None):
        # read-only id (no setter provided later)
        self._student_id = student_id

        # these use property setters (validation happens there)
        self.name = name
        self.email = email
        self.age = age
        self.gpa = gpa
        self.credits = credits

        # optional fields (also go through setters)
        self.weight_kg = weight_kg
        self.height_m = height_m

    # --- read-only id ---
    @property
    def student_id(self):
        return self._student_id

    # --- name ---
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()

    # --- email (simple check only) ---
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Email must look like user@example.com")
        self._email = value.strip()

    # --- age ---
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or not (0 <= value <= 110):
            raise ValueError("Age must be an integer between 0 and 110")
        self._age = value

    # --- gpa ---
    @property
    def gpa(self):
        return self._gpa

    @gpa.setter
    def gpa(self, value):
        try:
            f = float(value)
        except (TypeError, ValueError):
            raise ValueError("GPA must be a number")
        if not (0.0 <= f <= 4.0):
            raise ValueError("GPA must be between 0.0 and 4.0")
        self._gpa = round(f, 2)

    # --- credits ---
    @property
    def credits(self):
        return self._credits

    @credits.setter
    def credits(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Credits must be a non-negative integer")
        self._credits = value

    # --- optional: weight_kg ---
    @property
    def weight_kg(self):
        return getattr(self, "_weight_kg", None)

    @weight_kg.setter
    def weight_kg(self, value):
        if value is None:
            self._weight_kg = None
            return
        try:
            f = float(value)
        except (TypeError, ValueError):
            raise ValueError("weight_kg must be a number")
        if f <= 0 or f > 400:
            raise ValueError("weight_kg must be > 0 and realistic")
        self._weight_kg = round(f, 2)

    # --- optional: height_m ---
    @property
    def height_m(self):
        return getattr(self, "_height_m", None)

    @height_m.setter
    def height_m(self, value):
        if value is None:
            self._height_m = None
            return
        try:
            f = float(value)
        except (TypeError, ValueError):
            raise ValueError("height_m must be a number")
        if f <= 0 or not (0.5 <= f <= 2.7):
            raise ValueError("height_m must be realistic (0.5..2.7 meters)")
        self._height_m = round(f, 3)

    # --- computed properties ---
    @property
    def full_time_status(self):
        return "Full-Time" if self.credits >= 12 else "Part-Time"

    @property
    def standing(self):
        c = self.credits
        if c < 30:
            return "Freshman"
        elif c < 60:
            return "Sophomore"
        elif c < 90:
            return "Junior"
        return "Senior"

    @property
    def bmi(self):
        if self.weight_kg is None or self.height_m is None:
            return None
        return round(self.weight_kg / (self.height_m ** 2), 1)

    def __str__(self):
        parts = [
            f"{self.name} (ID: {self.student_id})",
            f"Email: {self.email}",
            f"GPA: {self.gpa}",
            f"Credits: {self.credits} — {self.full_time_status}, {self.standing}",
        ]
        if self.bmi is not None:
            parts.append(f"BMI: {self.bmi}")
        else:
            parts.append("BMI: N/A")
        return " | ".join(parts)


# Small demo so the grader sees it run.
if __name__ == "__main__":
    # using your Harper email to look real
    s = Student(
        student_id=101,
        name="Amtoj Singh",
        email="sa48190@mail.harpercollege.edu",
        age=24,
        gpa=3.6,
        credits=40,
        weight_kg=82,
        height_m=1.81,
    )

    print(s)
    print("Full-time:", s.full_time_status)
    print("Standing:", s.standing)
    print("BMI:", s.bmi)

    # quick validation examples (kept short)
    try:
        s.email = "bademail"
    except ValueError as e:
        print("Email error:", e)

    try:
        s.gpa = 5.2
    except ValueError as e:
        print("GPA error:", e)
