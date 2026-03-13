import pytest
from pydantic import ValidationError
from app.schemas.cafe import CafeCreate, CafeUpdate
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


# ── CafeCreate ─────────────────────────────────────────────────────────────

class TestCafeCreateValidation:
    def test_valid_cafe_passes(self):
        cafe = CafeCreate(name="The Grind", description="A great cafe", location="Orchard")
        assert cafe.name == "The Grind"

    def test_name_too_short_raises(self):
        with pytest.raises(ValidationError):
            CafeCreate(name="Hi", description="A great cafe", location="Orchard")

    def test_name_too_long_raises(self):
        with pytest.raises(ValidationError):
            CafeCreate(name="This Is Way Too Long", description="A great cafe", location="Orchard")

    def test_description_too_long_raises(self):
        with pytest.raises(ValidationError):
            CafeCreate(name="The Grind", description="A" * 257, location="Orchard")

    def test_missing_required_fields_raises(self):
        with pytest.raises(ValidationError):
            CafeCreate(name="The Grind")


# ── CafeUpdate ─────────────────────────────────────────────────────────────

class TestCafeUpdateValidation:
    def test_all_fields_optional(self):
        update = CafeUpdate()
        assert update.name is None
        assert update.description is None
        assert update.location is None

    def test_name_too_long_raises(self):
        with pytest.raises(ValidationError):
            CafeUpdate(name="This Is Way Too Long")

    def test_name_too_short_raises(self):
        with pytest.raises(ValidationError):
            CafeUpdate(name="Hi")


# ── EmployeeCreate ─────────────────────────────────────────────────────────

class TestEmployeeCreateValidation:
    def test_valid_employee_passes(self):
        employee = EmployeeCreate(
            name="Alice Tan",
            email_address="alice@example.com",
            phone_number="91234567",
            gender="Female",
        )
        assert employee.name == "Alice Tan"

    def test_name_too_short_raises(self):
        with pytest.raises(ValidationError):
            EmployeeCreate(
                name="Al",
                email_address="alice@example.com",
                phone_number="91234567",
                gender="Female",
            )

    def test_name_too_long_raises(self):
        with pytest.raises(ValidationError):
            EmployeeCreate(
                name="A Very Long Name",
                email_address="alice@example.com",
                phone_number="91234567",
                gender="Female",
            )

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            EmployeeCreate(
                name="Alice Tan",
                email_address="not-an-email",
                phone_number="91234567",
                gender="Female",
            )

    def test_phone_not_starting_with_8_or_9_raises(self):
        with pytest.raises(ValidationError):
            EmployeeCreate(
                name="Alice Tan",
                email_address="alice@example.com",
                phone_number="12345678",
                gender="Female",
            )

    def test_phone_too_short_raises(self):
        with pytest.raises(ValidationError):
            EmployeeCreate(
                name="Alice Tan",
                email_address="alice@example.com",
                phone_number="9123456",  # 7 digits
                gender="Female",
            )

    def test_invalid_gender_raises(self):
        with pytest.raises(ValidationError):
            EmployeeCreate(
                name="Alice Tan",
                email_address="alice@example.com",
                phone_number="91234567",
                gender="Other",
            )

    def test_valid_male_gender_passes(self):
        employee = EmployeeCreate(
            name="Bob Lim",
            email_address="bob@example.com",
            phone_number="81234567",
            gender="Male",
        )
        assert employee.gender == "Male"

    def test_cafe_id_is_optional(self):
        employee = EmployeeCreate(
            name="Alice Tan",
            email_address="alice@example.com",
            phone_number="91234567",
            gender="Female",
        )
        assert employee.cafe_id is None


# ── EmployeeUpdate ─────────────────────────────────────────────────────────

class TestEmployeeUpdateValidation:
    def test_all_fields_optional(self):
        update = EmployeeUpdate()
        assert update.name is None
        assert update.phone_number is None

    def test_invalid_phone_raises(self):
        with pytest.raises(ValidationError):
            EmployeeUpdate(phone_number="12345678")

    def test_valid_phone_passes(self):
        update = EmployeeUpdate(phone_number="91234567")
        assert update.phone_number == "91234567"
