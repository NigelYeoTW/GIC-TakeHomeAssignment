import uuid
from fastapi import UploadFile
from app.models.cafe import Cafe
from app.repositories.interfaces import CafeRepositoryInterface
from app.schemas.cafe import CafeCreate, CafeUpdate, CafeResponse
from app.utils.file_handler import save_logo, delete_logo
from app.utils.exceptions import NotFoundException
from app.utils.logger import get_logger
from app.utils.orm import orm_to_dict

logger = get_logger(__name__)


class CafeService:

    def __init__(self, repo: CafeRepositoryInterface):
        self.repo = repo

    def get_by_id(self, cafe_id: str) -> CafeResponse:
        cafe = self._get_or_404(cafe_id)
        count = self.repo.get_employee_count(cafe_id)
        return CafeResponse.model_validate({**orm_to_dict(cafe), "employees": count})

    def get_all(self, location: str | None) -> list[CafeResponse]:
        results = self.repo.get_all(location)
        return [
            CafeResponse.model_validate({**orm_to_dict(cafe), "employees": count})
            for cafe, count in results
        ]

    def create(self, payload: CafeCreate, logo: UploadFile | None) -> CafeResponse:
        logo_path = save_logo(logo) if logo else None
        cafe = Cafe(
            id=str(uuid.uuid4()),
            name=payload.name,
            description=payload.description,
            location=payload.location,
            logo=logo_path,
        )
        created = self.repo.create(cafe)
        return CafeResponse.model_validate({**orm_to_dict(created), "employees": 0})

    def update(self, cafe_id: str, payload: CafeUpdate, logo: UploadFile | None) -> CafeResponse:
        cafe = self._get_or_404(cafe_id)

        if payload.name is not None:
            cafe.name = payload.name
        if payload.description is not None:
            cafe.description = payload.description
        if payload.location is not None:
            cafe.location = payload.location
        if logo:
            if cafe.logo:
                delete_logo(cafe.logo)
            cafe.logo = save_logo(logo)

        updated = self.repo.update(cafe)
        count = self.repo.get_employee_count(cafe_id)
        return CafeResponse.model_validate({**orm_to_dict(updated), "employees": count})

    def delete(self, cafe_id: str) -> None:
        cafe = self._get_or_404(cafe_id)
        if cafe.logo:
            delete_logo(cafe.logo)
        self.repo.delete_with_employees(cafe)

    def _get_or_404(self, cafe_id: str) -> Cafe:
        cafe = self.repo.get_by_id(cafe_id)
        if not cafe:
            raise NotFoundException("Cafe", cafe_id)
        return cafe