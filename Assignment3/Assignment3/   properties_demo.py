"""
Assignment 3 – Properties
CIS 216 – Amtoj Singh

This program shows how to use properties in Python.
- Uses getters and setters with validation
- Has a read-only property (student_id)
- Has computed properties (full_time_status, standing, bmi)
"""

class Student:
    def __init__(self, student_id, name, email, age, gpa, credits, weight_kg=None, height_m=None):
        self._student_id = student_id      # read-only
        self.name = name
        self.email = email
        self.age = age
        self.gpa = gpa
        self.credits = credits
        self.weight_kg = weight_kg
        self.height_m = height_m

    # read-only property
    @property
    def student_id(self):
        return self._student_id

    # name with validation
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.title()

    # email with validation (basic check)
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Email must contain @")
        self._email = value

    # age
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not (0 <= value <= 110):
            raise ValueError("Age must be between 0 and 110")
        self._age = value

    # gpa
    @property
    def gpa(self):
        return self._gpa

    @gpa.setter
    def gpa(self, value):
        if not (0.0 <= value <= 4.0):
            raise ValueError("GPA must be between 0.0 and 4.0")
        self._gpa = round(value, 2)

    # credits
    @property
    def credits(self):
        return self._credits

    @credits.setter
    def credits(self, value):
        if value < 0:
            raise ValueError("Credits cannot be negative")
        self._credits = value

    # computed property: full-time / part-time
    @property
    def full_time_status(self):
        return "Full-Time" if self.credits >= 12 else "Part-Time"

    # computed property: standing
    @property
    def standing(self):
        if self.credits < 30:
            return "Freshman"
        elif self.credits < 60:
            return "Sophomore"
        elif self.credits < 90:
            return "Junior"
        else:
            return "Senior"

    # bmi (optional, only if height and weight given)
    @property
    def bmi(self):
        if self.weight_kg and self.height_m:
            return round(self.weight_kg / (self.height_m ** 2), 1)
        return None

    def __str__(self):
        return f"{self.name} ({self.student_id}) - GPA: {self.gpa}, Credits: {self.credits}, Standing: {self.standing}"


# demo
if __name__ == "__main__":
    student = Student(101, "amtoj singh", "amtoj@example.com", 24, 3.6, 40, 82, 1.81)
    print(student)
    print("Full-time status:", student.full_time_status)
    print("BMI:", student.bmi)

    # show validation
    try:
        student.age = 150
    except ValueError as e:
        print("Error:", e)

