import pytest
from app.schemas.employee import EmployeeMutationResponse
from app.utils.exceptions import NotFoundException, ConflictException
from tests.conftest import CAFE_ID, EMPLOYEE_ID, EMPLOYEE_RESPONSE, EMPLOYEE_MUTATION_RESPONSE, EMPLOYEE_DELETE_RESPONSE


VALID_EMPLOYEE_PAYLOAD = {
    "name": "Alice Tan",
    "email_address": "alice@example.com",
    "phone_number": "91234567",
    "gender": "Female",
    "cafe_id": None,
}


class TestGetEmployees:
    def test_returns_all_employees(self, client, mock_employee_service):
        mock_employee_service.get_all.return_value = [EMPLOYEE_RESPONSE]

        response = client.get("/api/v1/employees")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == EMPLOYEE_ID
        assert data[0]["days_worked"] == 30

    def test_returns_empty_list_when_no_employees(self, client, mock_employee_service):
        mock_employee_service.get_all.return_value = []

        response = client.get("/api/v1/employees")

        assert response.status_code == 200
        assert response.json() == []

    def test_passes_cafe_filter(self, client, mock_employee_service):
        mock_employee_service.get_all.return_value = [EMPLOYEE_RESPONSE]

        response = client.get("/api/v1/employees?cafe=The Grind")

        assert response.status_code == 200
        mock_employee_service.get_all.assert_called_once_with("The Grind")

    def test_returns_empty_list_for_invalid_cafe(self, client, mock_employee_service):
        mock_employee_service.get_all.return_value = []

        response = client.get("/api/v1/employees?cafe=NonexistentCafe")

        assert response.status_code == 200
        assert response.json() == []


class TestCreateEmployee:
    def test_creates_employee_successfully(self, client, mock_employee_service):
        mock_employee_service.create.return_value = EMPLOYEE_MUTATION_RESPONSE

        response = client.post("/api/v1/employees", json=VALID_EMPLOYEE_PAYLOAD)

        assert response.status_code == 201
        assert response.json()["employee"]["id"] == EMPLOYEE_ID

    def test_creates_employee_with_cafe_assignment(self, client, mock_employee_service):
        assigned = EMPLOYEE_RESPONSE.model_copy(update={"cafe": "The Grind"})
        mock_employee_service.create.return_value = EmployeeMutationResponse(employee=assigned, affected_cafes=[])

        payload = {**VALID_EMPLOYEE_PAYLOAD, "cafe_id": CAFE_ID}
        response = client.post("/api/v1/employees", json=payload)

        assert response.status_code == 201
        assert response.json()["employee"]["cafe"] == "The Grind"

    def test_returns_409_when_email_already_exists(self, client, mock_employee_service):
        mock_employee_service.create.side_effect = ConflictException(
            "An employee with this email already exists"
        )

        response = client.post("/api/v1/employees", json=VALID_EMPLOYEE_PAYLOAD)

        assert response.status_code == 409

    def test_returns_404_when_cafe_not_found(self, client, mock_employee_service):
        mock_employee_service.create.side_effect = NotFoundException("Cafe", "nonexistent-id")

        payload = {**VALID_EMPLOYEE_PAYLOAD, "cafe_id": "nonexistent-id"}
        response = client.post("/api/v1/employees", json=payload)

        assert response.status_code == 404


class TestUpdateEmployee:
    def test_updates_employee_successfully(self, client, mock_employee_service):
        updated = EMPLOYEE_RESPONSE.model_copy(update={"name": "Alice New"})
        mock_employee_service.update.return_value = EmployeeMutationResponse(employee=updated, affected_cafes=[])

        response = client.put(f"/api/v1/employees/{EMPLOYEE_ID}", json={"name": "Alice New"})

        assert response.status_code == 200
        assert response.json()["employee"]["name"] == "Alice New"

    def test_reassigns_employee_to_new_cafe(self, client, mock_employee_service):
        updated = EMPLOYEE_RESPONSE.model_copy(update={"cafe": "Brew & Co", "days_worked": 0})
        mock_employee_service.update.return_value = EmployeeMutationResponse(employee=updated, affected_cafes=[])

        response = client.put(
            f"/api/v1/employees/{EMPLOYEE_ID}",
            json={"cafe_id": CAFE_ID}
        )

        assert response.status_code == 200
        assert response.json()["employee"]["days_worked"] == 0

    def test_returns_404_when_employee_not_found(self, client, mock_employee_service):
        missing_id = "UIAAAAAAA"
        mock_employee_service.update.side_effect = NotFoundException("Employee", missing_id)

        response = client.put(f"/api/v1/employees/{missing_id}", json={"name": "Alice New"})

        assert response.status_code == 404


class TestDeleteEmployee:
    def test_deletes_employee_successfully(self, client, mock_employee_service):
        mock_employee_service.delete.return_value = EMPLOYEE_DELETE_RESPONSE

        response = client.delete(f"/api/v1/employees/{EMPLOYEE_ID}")

        assert response.status_code == 200
        mock_employee_service.delete.assert_called_once_with(EMPLOYEE_ID)

    def test_returns_404_when_employee_not_found(self, client, mock_employee_service):
        missing_id = "UIAAAAAAA"
        mock_employee_service.delete.side_effect = NotFoundException("Employee", missing_id)

        response = client.delete(f"/api/v1/employees/{missing_id}")

        assert response.status_code == 404