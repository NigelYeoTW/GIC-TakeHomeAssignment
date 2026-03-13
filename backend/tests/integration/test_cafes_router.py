import pytest
from app.utils.exceptions import NotFoundException
from tests.conftest import CAFE_ID, CAFE_RESPONSE


class TestGetCafes:
    def test_returns_all_cafes(self, client, mock_cafe_service):
        mock_cafe_service.get_all.return_value = [CAFE_RESPONSE]

        response = client.get("/api/v1/cafes")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "The Grind"
        assert data[0]["employees"] == 2

    def test_returns_empty_list_when_no_cafes(self, client, mock_cafe_service):
        mock_cafe_service.get_all.return_value = []

        response = client.get("/api/v1/cafes")

        assert response.status_code == 200
        assert response.json() == []

    def test_passes_location_filter(self, client, mock_cafe_service):
        mock_cafe_service.get_all.return_value = [CAFE_RESPONSE]

        response = client.get("/api/v1/cafes?location=Orchard")

        assert response.status_code == 200
        mock_cafe_service.get_all.assert_called_once_with("Orchard")

    def test_returns_empty_list_for_invalid_location(self, client, mock_cafe_service):
        mock_cafe_service.get_all.return_value = []

        response = client.get("/api/v1/cafes?location=InvalidPlace")

        assert response.status_code == 200
        assert response.json() == []


class TestCreateCafe:
    def test_creates_cafe_successfully(self, client, mock_cafe_service):
        mock_cafe_service.create.return_value = CAFE_RESPONSE

        response = client.post("/api/v1/cafes", data={
            "name": "The Grind",
            "description": "Specialty coffee in the heart of the city",
            "location": "Orchard",
        })

        assert response.status_code == 201
        assert response.json()["name"] == "The Grind"


class TestUpdateCafe:
    def test_updates_cafe_successfully(self, client, mock_cafe_service):
        updated = CAFE_RESPONSE.model_copy(update={"location": "Bugis"})
        mock_cafe_service.update.return_value = updated

        response = client.put(f"/api/v1/cafes/{CAFE_ID}", data={"location": "Bugis"})

        assert response.status_code == 200
        assert response.json()["location"] == "Bugis"

    def test_returns_404_when_cafe_not_found(self, client, mock_cafe_service):
        missing_id = "00000000-0000-0000-0000-000000000000"
        mock_cafe_service.update.side_effect = NotFoundException("Cafe", missing_id)

        response = client.put(f"/api/v1/cafes/{missing_id}", data={"location": "Bugis"})

        assert response.status_code == 404


class TestDeleteCafe:
    def test_deletes_cafe_successfully(self, client, mock_cafe_service):
        mock_cafe_service.delete.return_value = None

        response = client.delete(f"/api/v1/cafes/{CAFE_ID}")

        assert response.status_code == 204
        mock_cafe_service.delete.assert_called_once_with(CAFE_ID)

    def test_returns_404_when_cafe_not_found(self, client, mock_cafe_service):
        missing_id = "00000000-0000-0000-0000-000000000000"
        mock_cafe_service.delete.side_effect = NotFoundException("Cafe", missing_id)

        response = client.delete(f"/api/v1/cafes/{missing_id}")

        assert response.status_code == 404