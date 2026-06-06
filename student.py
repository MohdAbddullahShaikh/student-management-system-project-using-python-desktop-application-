"""
student.py - Student data model for Student Management System.
Provides a lightweight dataclass-style object and validation helpers.
"""

from datetime import date, datetime


class Student:
    """Represents a single student record."""

    GENDERS = ("Male", "Female", "Other", "Prefer not to say")

    COURSES = (
        "Computer Science",
        "Information Technology",
        "Electronics Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Business Administration",
        "Commerce",
        "Arts & Humanities",
        "Biology / Life Sciences",
        "Physics",
        "Mathematics",
        "Other",
    )

    def __init__(
        self,
        student_id=None,
        name="",
        age=None,
        gender="",
        course="",
        email="",
        phone="",
        address="",
        admission_date=None,
    ):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.course = course
        self.email = email
        self.phone = phone
        self.address = address
        self.admission_date = admission_date or date.today()

    # ─────────────────────────────────────────────
    # Validation helpers
    # ─────────────────────────────────────────────

    @staticmethod
    def validate(name, age_str, email, phone):
        """
        Validate required fields.
        Returns (True, "") on success or (False, error_message) on failure.
        """
        errors = []

        if not name.strip():
            errors.append("• Name is required.")

        if not age_str.strip():
            errors.append("• Age is required.")
        else:
            try:
                age = int(age_str)
                if not (1 <= age <= 120):
                    errors.append("• Age must be between 1 and 120.")
            except ValueError:
                errors.append("• Age must be a whole number.")

        if email.strip():
            if "@" not in email or "." not in email.split("@")[-1]:
                errors.append("• Enter a valid email address.")

        if phone.strip():
            digits = phone.replace("+", "").replace("-", "").replace(" ", "")
            if not digits.isdigit() or not (7 <= len(digits) <= 15):
                errors.append("• Phone must be 7–15 digits (spaces/dashes/+ allowed).")

        if errors:
            return False, "\n".join(errors)
        return True, ""

    @staticmethod
    def parse_date(date_str):
        """Parse a date string in YYYY-MM-DD format; return a date object."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Admission date must be in YYYY-MM-DD format.")

    # ─────────────────────────────────────────────
    # Factory / conversion helpers
    # ─────────────────────────────────────────────

    @classmethod
    def from_row(cls, row):
        """Create a Student instance from a database row tuple."""
        return cls(
            student_id=row[0],
            name=row[1],
            age=row[2],
            gender=row[3],
            course=row[4],
            email=row[5],
            phone=row[6],
            address=row[7],
            admission_date=row[8],
        )

    def to_tuple(self):
        """Return a tuple suitable for Treeview insertion (excluding student_id)."""
        return (
            self.student_id,
            self.name,
            self.age,
            self.gender,
            self.course,
            self.email,
            self.phone,
            self.address,
            str(self.admission_date) if self.admission_date else "",
        )

    def __repr__(self):
        return (
            f"Student(id={self.student_id}, name={self.name!r}, "
            f"age={self.age}, course={self.course!r})"
        )
