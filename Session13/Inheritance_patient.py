# ------------------------------------------------------------
# CIS 206 – Session 13
# Inheritance and Overriding
#
# Using last week's Patient class as a base, we create an
# Inpatient subclass that:
#   1) Inherits from Patient
#   2) Adds new attributes + a new method
#   3) Overrides a method from the base class
#   4) Is tested by creating objects and printing results
# ------------------------------------------------------------

# ------------ Base class from previous week: Patient ----------

class Patient:
    """Base Patient class from Session 12."""

    def __init__(
        self,
        first_name,
        middle_name,
        last_name,
        address,
        city,
        state,
        zip_code,
        phone,
        emergency_name,
        emergency_phone,
    ):
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name
        self._address = address
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._phone = phone
        self._emergency_name = emergency_name
        self._emergency_phone = emergency_phone

    # Accessors (just the ones we really use here)

    def get_full_name(self):
        middle = f" {self._middle_name}" if self._middle_name else ""
        return f"{self._first_name}{middle} {self._last_name}"

    def get_address(self):
        return self._address

    def get_city_state_zip(self):
        return f"{self._city}, {self._state} {self._zip_code}"

    def get_phone(self):
        return self._phone

    def get_emergency_contact(self):
        return f"{self._emergency_name} ({self._emergency_phone})"

    def __str__(self):
        """String representation of a basic patient record."""
        lines = [
            f"Patient Name:     {self.get_full_name()}",
            f"Address:          {self.get_address()}",
            f"City/State/Zip:   {self.get_city_state_zip()}",
            f"Phone:            {self.get_phone()}",
            f"Emergency Contact:{self.get_emergency_contact()}",
        ]
        return "\n".join(lines)


# --------- Derived class: Inpatient (Inheritance + Override) ---------

class Inpatient(Patient):
    """
    Inpatient is a specialized Patient who is admitted to the hospital.

    Inheritance:
        Inherits all fields and behavior from Patient.

    Additions:
        - room_number
        - length_of_stay_days
        - daily_rate

    New method:
        - calculate_stay_cost()

    Overriding:
        - __str__ is overridden to show extra inpatient details.
    """

    def __init__(
        self,
        first_name,
        middle_name,
        last_name,
        address,
        city,
        state,
        zip_code,
        phone,
        emergency_name,
        emergency_phone,
        room_number,
        length_of_stay_days,
        daily_rate,
    ):
        # Call base class constructor to set all the patient info
        super().__init__(
            first_name,
            middle_name,
            last_name,
            address,
            city,
            state,
            zip_code,
            phone,
            emergency_name,
            emergency_phone,
        )
        # New attributes for the subclass
        self._room_number = room_number
        self._length_of_stay_days = length_of_stay_days
        self._daily_rate = daily_rate

    # New method (required by assignment)
    def calculate_stay_cost(self):
        """Return total bill for the stay based on days * daily_rate."""
        return self._length_of_stay_days * self._daily_rate

    # Overridden method (required by assignment)
    def __str__(self):
        """
        Override the base __str__ so we still show the normal
        patient info plus the inpatient-specific details.
        """
        base_info = super().__str__()  # call Patient.__str__()
        total_cost = self.calculate_stay_cost()
        extra_lines = [
            f"Room Number:      {self._room_number}",
            f"Length of Stay:   {self._length_of_stay_days} day(s)",
            f"Daily Rate:       ${self._daily_rate:,.2f}",
            f"Total Stay Cost:  ${total_cost:,.2f}",
        ]
        return base_info + "\n" + "\n".join(extra_lines)


# ---------------------- Test / Demo code ----------------------

def demo_inheritance_and_overriding():
    print("=== Session 13 – Inheritance and Overriding Demo ===\n")

    # Base patient (from Session 12 style)
    basic_patient = Patient(
        first_name="John",
        middle_name="A.",
        last_name="Doe",
        address="123 Main St",
        city="Chicago",
        state="IL",
        zip_code="60007",
        phone="847-555-1234",
        emergency_name="Jane Doe",
        emergency_phone="847-555-5678",
    )

    print("Basic Patient (base class):")
    print(basic_patient)
    print("\n" + "-" * 55 + "\n")

    # Inpatient (derived class)
    inpatient = Inpatient(
        first_name="Sarah",
        middle_name="M.",
        last_name="Lopez",
        address="456 Oak Ave",
        city="Schaumburg",
        state="IL",
        zip_code="60193",
        phone="847-555-7777",
        emergency_name="Carlos Lopez",
        emergency_phone="847-555-9999",
        room_number="402B",
        length_of_stay_days=5,
        daily_rate=750.00,
    )

    print("Inpatient (derived class with extra behavior):")
    print(inpatient)
    print("\nCalculated stay cost using new method:")
    print(f"  -> ${inpatient.calculate_stay_cost():,.2f}")


if __name__ == "__main__":
    demo_inheritance_and_overriding()
