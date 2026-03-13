import pytest
from typing import Generator
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_cafe_service, get_employee_service
from app.repositories.interfaces import CafeRepositoryInterface, EmployeeRepositoryInterface
from app.services.cafe_service import CafeService
from app.services.employee_service import EmployeeService
from app.schemas.cafe import CafeResponse
from app.schemas.employee import EmployeeResponse, EmployeeMutationResponse


# ── Shared test data constants ─────────────────────────────────────────────

CAFE_ID = "550e8400-e29b-41d4-a716-446655440000"
EMPLOYEE_ID = "UIAB12345"

CAFE_RESPONSE = CafeResponse(
    id=CAFE_ID,
    name="The Grind",
    description="Specialty coffee in the heart of the city",
    logo=None,
    location="Orchard",
    employees=2,
)

EMPLOYEE_RESPONSE = EmployeeResponse(
    id=EMPLOYEE_ID,
    name="Alice Tan",
    email_address="alice@example.com",
    phone_number="91234567",
    gender="Female",
    days_worked=30,
    cafe="The Grind",
)

EMPLOYEE_MUTATION_RESPONSE = EmployeeMutationResponse(
    employee=EMPLOYEE_RESPONSE,
    affected_cafes=[],
)

EMPLOYEE_DELETE_RESPONSE = EmployeeMutationResponse(
    employee=None,
    affected_cafes=[],
)


# ── Service mocks ──────────────────────────────────────────────────────────

@pytest.fixture
def mock_cafe_service() -> MagicMock:
    return MagicMock(spec=CafeService)


@pytest.fixture
def mock_employee_service() -> MagicMock:
    return MagicMock(spec=EmployeeService)


# ── Test client with overridden dependencies ───────────────────────────────

@pytest.fixture
def client(mock_cafe_service, mock_employee_service) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_cafe_service] = lambda: mock_cafe_service
    app.dependency_overrides[get_employee_service] = lambda: mock_employee_service
    yield TestClient(app)
    app.dependency_overrides.clear()


# ── Repository mocks for unit tests ───────────────────────────────────────

@pytest.fixture
def mock_cafe_repo() -> MagicMock:
    return MagicMock(spec=CafeRepositoryInterface)


@pytest.fixture
def mock_employee_repo() -> MagicMock:
    return MagicMock(spec=EmployeeRepositoryInterface)
