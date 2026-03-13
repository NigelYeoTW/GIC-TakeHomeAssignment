import pytest
from unittest.mock import MagicMock, patch
from app.models.cafe import Cafe
from app.services.cafe_service import CafeService
from app.schemas.cafe import CafeCreate, CafeUpdate, CafeResponse
from app.utils.exceptions import NotFoundException
from tests.conftest import CAFE_ID


CAFE_DICT = {
    "id": CAFE_ID,
    "name": "The Grind",
    "description": "Specialty coffee in the heart of the city",
    "logo": None,
    "location": "Orchard",
}


# ── Helpers ────────────────────────────────────────────────────────────────

def make_cafe_model(**kwargs) -> MagicMock:
    cafe = MagicMock(spec=Cafe)
    cafe.id = CAFE_ID
    cafe.name = "The Grind"
    cafe.description = "Specialty coffee in the heart of the city"
    cafe.logo = None
    cafe.location = "Orchard"
    cafe.assignments = []
    for k, v in kwargs.items():
        setattr(cafe, k, v)
    return cafe


# ── get_all ────────────────────────────────────────────────────────────────

class TestGetAll:
    def test_returns_list_of_cafe_responses(self, mock_cafe_repo):
        cafe = make_cafe_model()
        mock_cafe_repo.get_all.return_value = [(cafe, 2)]
        service = CafeService(mock_cafe_repo)

        with patch("app.services.cafe_service.orm_to_dict", return_value=CAFE_DICT):
            result = service.get_all(location=None)

        assert len(result) == 1
        assert isinstance(result[0], CafeResponse)
        assert result[0].employees == 2

    def test_passes_location_filter_to_repo(self, mock_cafe_repo):
        mock_cafe_repo.get_all.return_value = []
        service = CafeService(mock_cafe_repo)

        service.get_all(location="Orchard")

        mock_cafe_repo.get_all.assert_called_once_with("Orchard")

    def test_returns_empty_list_when_no_cafes(self, mock_cafe_repo):
        mock_cafe_repo.get_all.return_value = []
        service = CafeService(mock_cafe_repo)

        result = service.get_all(location=None)

        assert result == []


# ── create ─────────────────────────────────────────────────────────────────

class TestCreate:
    def test_creates_cafe_without_logo(self, mock_cafe_repo):
        payload = CafeCreate(name="The Grind", description="A great cafe", location="Orchard")
        cafe = make_cafe_model()
        mock_cafe_repo.create.return_value = cafe
        service = CafeService(mock_cafe_repo)

        with patch("app.services.cafe_service.orm_to_dict", return_value=CAFE_DICT):
            result = service.create(payload, logo=None)

        assert isinstance(result, CafeResponse)
        assert result.employees == 0
        mock_cafe_repo.create.assert_called_once()

    def test_creates_cafe_with_logo(self, mock_cafe_repo):
        payload = CafeCreate(name="The Grind", description="A great cafe", location="Orchard")
        cafe = make_cafe_model(logo="uploads/logo.png")
        mock_cafe_repo.create.return_value = cafe
        mock_logo = MagicMock()
        service = CafeService(mock_cafe_repo)

        with patch("app.services.cafe_service.save_logo", return_value="uploads/logo.png"), \
             patch("app.services.cafe_service.orm_to_dict", return_value={**CAFE_DICT, "logo": "uploads/logo.png"}):
            result = service.create(payload, logo=mock_logo)

        assert result.logo == "uploads/logo.png"


# ── update ─────────────────────────────────────────────────────────────────

class TestUpdate:
    def test_updates_cafe_fields(self, mock_cafe_repo):
        cafe = make_cafe_model()
        mock_cafe_repo.get_by_id.return_value = cafe
        mock_cafe_repo.update.return_value = cafe
        mock_cafe_repo.get_employee_count.return_value = 2
        service = CafeService(mock_cafe_repo)

        payload = CafeUpdate(name="New Name", location="Bugis")
        with patch("app.services.cafe_service.orm_to_dict", return_value={**CAFE_DICT, "name": "New Name", "location": "Bugis"}):
            service.update(CAFE_ID, payload, logo=None)

        assert cafe.name == "New Name"
        assert cafe.location == "Bugis"

    def test_raises_404_when_cafe_not_found(self, mock_cafe_repo):
        mock_cafe_repo.get_by_id.return_value = None
        service = CafeService(mock_cafe_repo)

        with pytest.raises(NotFoundException):
            service.update("nonexistent-id", CafeUpdate(), logo=None)


# ── delete ─────────────────────────────────────────────────────────────────

class TestDelete:
    def test_deletes_cafe(self, mock_cafe_repo):
        cafe = make_cafe_model()
        mock_cafe_repo.get_by_id.return_value = cafe
        service = CafeService(mock_cafe_repo)

        service.delete(CAFE_ID)

        mock_cafe_repo.delete.assert_called_once_with(cafe)

    def test_raises_404_when_cafe_not_found(self, mock_cafe_repo):
        mock_cafe_repo.get_by_id.return_value = None
        service = CafeService(mock_cafe_repo)

        with pytest.raises(NotFoundException):
            service.delete("nonexistent-id")

    def test_deletes_logo_file_when_exists(self, mock_cafe_repo):
        cafe = make_cafe_model(logo="uploads/logo.png")
        mock_cafe_repo.get_by_id.return_value = cafe
        service = CafeService(mock_cafe_repo)

        with patch("app.services.cafe_service.delete_logo") as mock_delete:
            service.delete(CAFE_ID)
            mock_delete.assert_called_once_with("uploads/logo.png")