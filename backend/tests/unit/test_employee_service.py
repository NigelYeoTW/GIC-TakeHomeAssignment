import pytest
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from app.models.employee import Employee
from app.models.cafe_employee import CafeEmployee
from app.models.cafe import Cafe
from app.services.employee_service import EmployeeService
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeMutationResponse
from app.utils.exceptions import NotFoundException
from tests.conftest import CAFE_ID, EMPLOYEE_ID


# ── Helpers ────────────────────────────────────────────────────────────────

EMPLOYEE_DICT = {
    "id": EMPLOYEE_ID,
    "name": "Alice Tan",
    "email_address": "alice@example.com",
    "phone_number": "91234567",
    "gender": "Female",
}


def make_employee_model(**kwargs) -> MagicMock:
    employee = MagicMock(spec=Employee)
    employee.id = EMPLOYEE_ID
    employee.name = "Alice Tan"
    employee.email_address = "alice@example.com"
    employee.phone_number = "91234567"
    employee.gender = "Female"
    for k, v in kwargs.items():
        setattr(employee, k, v)
    return employee


def make_assignment_model(days_ago: int = 30, cafe_id: str = "other-cafe-id") -> MagicMock:
    assignment = MagicMock(spec=CafeEmployee)
    assignment.start_date = date.today() - timedelta(days=days_ago)
    assignment.cafe_id = cafe_id
    assignment.cafe = MagicMock(spec=Cafe)
    assignment.cafe.name = "The Grind"
    return assignment


def make_cafe_model() -> MagicMock:
    cafe = MagicMock(spec=Cafe)
    cafe.id = CAFE_ID
    cafe.name = "The Grind"
    return cafe


# ── get_all ────────────────────────────────────────────────────────────────

class TestGetAll:
    def test_returns_list_of_employee_responses(self, mock_employee_repo, mock_cafe_repo):
        employee = make_employee_model()
        mock_employee_repo.get_all.return_value = [(employee, 30, "The Grind")]
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        with patch("app.services.employee_service.orm_to_dict", return_value=EMPLOYEE_DICT):
            result = service.get_all(cafe_name=None)

        assert len(result) == 1
        assert isinstance(result[0], EmployeeResponse)
        assert result[0].days_worked == 30
        assert result[0].cafe == "The Grind"

    def test_returns_empty_list_when_no_employees(self, mock_employee_repo, mock_cafe_repo):
        mock_employee_repo.get_all.return_value = []
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        result = service.get_all(cafe_name=None)

        assert result == []

    def test_passes_cafe_name_filter_to_repo(self, mock_employee_repo, mock_cafe_repo):
        mock_employee_repo.get_all.return_value = []
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        service.get_all(cafe_name="The Grind")

        mock_employee_repo.get_all.assert_called_once_with("The Grind")


# ── create ─────────────────────────────────────────────────────────────────

class TestCreate:
    def test_creates_unassigned_employee(self, mock_employee_repo, mock_cafe_repo):
        payload = EmployeeCreate(
            name="Alice Tan",
            email_address="alice@example.com",
            phone_number="91234567",
            gender="Female",
            cafe_id=None,
        )
        employee = make_employee_model()
        mock_employee_repo.create_with_optional_assignment.return_value = employee
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        with patch("app.services.employee_service.orm_to_dict", return_value=EMPLOYEE_DICT):
            result = service.create(payload)

        assert isinstance(result, EmployeeMutationResponse)
        assert result.employee.cafe is None
        assert result.employee.days_worked == 0
        assert result.affected_cafes == []

    def test_creates_employee_with_cafe_assignment(self, mock_employee_repo, mock_cafe_repo):
        payload = EmployeeCreate(
            name="Alice Tan",
            email_address="alice@example.com",
            phone_number="91234567",
            gender="Female",
            cafe_id=CAFE_ID,
        )
        employee = make_employee_model()
        cafe = make_cafe_model()
        mock_employee_repo.create_with_optional_assignment.return_value = employee
        mock_cafe_repo.get_by_id.return_value = cafe
        mock_cafe_repo.get_employee_count.return_value = 3
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        with patch("app.services.employee_service.orm_to_dict", return_value=EMPLOYEE_DICT):
            result = service.create(payload)

        assert result.employee.cafe == "The Grind"
        assert len(result.affected_cafes) == 1
        assert result.affected_cafes[0].id == CAFE_ID
        mock_employee_repo.create_with_optional_assignment.assert_called_once()

    def test_raises_404_when_cafe_not_found(self, mock_employee_repo, mock_cafe_repo):
        payload = EmployeeCreate(
            name="Alice Tan",
            email_address="alice@example.com",
            phone_number="91234567",
            gender="Female",
            cafe_id="nonexistent-cafe-id",
        )
        mock_cafe_repo.get_by_id.return_value = None
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        with pytest.raises(NotFoundException):
            service.create(payload)


# ── update ─────────────────────────────────────────────────────────────────

class TestUpdate:
    def test_updates_employee_fields(self, mock_employee_repo, mock_cafe_repo):
        employee = make_employee_model()
        mock_employee_repo.get_by_id.return_value = employee
        mock_employee_repo.get_assignment.return_value = None
        mock_employee_repo.update.return_value = employee
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        payload = EmployeeUpdate(name="Bob Smith", gender="Male")
        with patch("app.services.employee_service.orm_to_dict", return_value={**EMPLOYEE_DICT, "name": "Bob Smith", "gender": "Male"}):
            service.update(EMPLOYEE_ID, payload)

        assert employee.name == "Bob Smith"
        assert employee.gender == "Male"

    def test_reassigns_employee_to_new_cafe(self, mock_employee_repo, mock_cafe_repo):
        employee = make_employee_model()
        existing_assignment = make_assignment_model(cafe_id="old-cafe-id")
        cafe = make_cafe_model()
        mock_employee_repo.get_by_id.return_value = employee
        mock_employee_repo.get_assignment.return_value = existing_assignment
        mock_employee_repo.update.return_value = employee
        mock_cafe_repo.get_by_id.return_value = cafe
        mock_cafe_repo.get_employee_count.return_value = 5
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        payload = EmployeeUpdate(cafe_id=CAFE_ID)
        with patch("app.services.employee_service.orm_to_dict", return_value=EMPLOYEE_DICT):
            result = service.update(EMPLOYEE_ID, payload)

        mock_employee_repo.reassign_cafe.assert_called_once_with(existing_assignment, EMPLOYEE_ID, CAFE_ID)
        assert result.employee.days_worked == 0

    def test_keeps_existing_days_worked_when_no_cafe_change(self, mock_employee_repo, mock_cafe_repo):
        employee = make_employee_model()
        assignment = make_assignment_model(days_ago=45)
        mock_employee_repo.get_by_id.return_value = employee
        mock_employee_repo.get_assignment.return_value = assignment
        mock_employee_repo.update.return_value = employee
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        payload = EmployeeUpdate(name="Alice New")
        with patch("app.services.employee_service.orm_to_dict", return_value={**EMPLOYEE_DICT, "name": "Alice New"}):
            result = service.update(EMPLOYEE_ID, payload)

        assert result.employee.days_worked == 45

    def test_raises_404_when_employee_not_found(self, mock_employee_repo, mock_cafe_repo):
        mock_employee_repo.get_by_id.return_value = None
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        with pytest.raises(NotFoundException):
            service.update("nonexistent-id", EmployeeUpdate())


# ── delete ─────────────────────────────────────────────────────────────────

class TestDelete:
    def test_deletes_employee(self, mock_employee_repo, mock_cafe_repo):
        employee = make_employee_model()
        mock_employee_repo.get_by_id.return_value = employee
        mock_employee_repo.get_assignment.return_value = None
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        result = service.delete(EMPLOYEE_ID)

        mock_employee_repo.delete.assert_called_once_with(employee)
        assert isinstance(result, EmployeeMutationResponse)
        assert result.employee is None
        assert result.affected_cafes == []

    def test_deletes_employee_updates_cafe_count(self, mock_employee_repo, mock_cafe_repo):
        employee = make_employee_model()
        assignment = make_assignment_model(cafe_id=CAFE_ID)
        mock_employee_repo.get_by_id.return_value = employee
        mock_employee_repo.get_assignment.return_value = assignment
        mock_cafe_repo.get_employee_count.return_value = 2
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        result = service.delete(EMPLOYEE_ID)

        assert len(result.affected_cafes) == 1
        assert result.affected_cafes[0].id == CAFE_ID

    def test_raises_404_when_employee_not_found(self, mock_employee_repo, mock_cafe_repo):
        mock_employee_repo.get_by_id.return_value = None
        service = EmployeeService(mock_employee_repo, mock_cafe_repo)

        with pytest.raises(NotFoundException):
            service.delete("nonexistent-id")
