from datetime import datetime, timezone
from app.models.employee import Employee
from app.repositories.interfaces import EmployeeRepositoryInterface, CafeRepositoryInterface
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeMutationResponse, CafeCountUpdate
from app.utils.exceptions import NotFoundException
from app.utils.logger import get_logger
from app.utils.orm import orm_to_dict

logger = get_logger(__name__)


class EmployeeService:

    def __init__(self, employee_repo: EmployeeRepositoryInterface, cafe_repo: CafeRepositoryInterface):
        self.employee_repo = employee_repo
        self.cafe_repo = cafe_repo

    def get_all(self, cafe_name: str | None) -> list[EmployeeResponse]:
        results = self.employee_repo.get_all(cafe_name)
        return [
            EmployeeResponse.model_validate({**orm_to_dict(employee), "days_worked": days_worked, "cafe": fetched_cafe_name})
            for employee, days_worked, fetched_cafe_name in results
        ]

    def create(self, payload: EmployeeCreate) -> EmployeeMutationResponse:
        cafe = self._get_cafe_or_404(payload.cafe_id) if payload.cafe_id else None

        employee = Employee(
            name=payload.name,
            email_address=payload.email_address,
            phone_number=payload.phone_number,
            gender=payload.gender,
        )
        created = self.employee_repo.create_with_optional_assignment(employee, payload.cafe_id)

        affected_cafes = []
        cafe_name = None
        if payload.cafe_id and cafe:
            count = self.cafe_repo.get_employee_count(payload.cafe_id)
            affected_cafes.append(CafeCountUpdate(id=payload.cafe_id, employees=count))
            cafe_name = cafe.name

        employee_response = EmployeeResponse.model_validate({**orm_to_dict(created), "days_worked": 0, "cafe": cafe_name})
        return EmployeeMutationResponse(employee=employee_response, affected_cafes=affected_cafes)

    def update(self, employee_id: str, payload: EmployeeUpdate) -> EmployeeMutationResponse:
        employee = self._get_or_404(employee_id)

        if payload.name is not None:
            employee.name = payload.name
        if payload.email_address is not None:
            employee.email_address = payload.email_address
        if payload.phone_number is not None:
            employee.phone_number = payload.phone_number
        if payload.gender is not None:
            employee.gender = payload.gender

        existing_assignment = self.employee_repo.get_assignment(employee_id)
        affected_cafes = []

        if payload.cafe_id is not None:
            cafe = self._get_cafe_or_404(payload.cafe_id)
            old_cafe_id = existing_assignment.cafe_id if existing_assignment else None
            self.employee_repo.reassign_cafe(existing_assignment, employee_id, payload.cafe_id)
            new_count = self.cafe_repo.get_employee_count(payload.cafe_id)
            affected_cafes.append(CafeCountUpdate(id=payload.cafe_id, employees=new_count))
            
            if old_cafe_id and old_cafe_id != payload.cafe_id:
                old_count = self.cafe_repo.get_employee_count(old_cafe_id)
                affected_cafes.append(CafeCountUpdate(id=old_cafe_id, employees=old_count))

            days_worked = 0
            cafe_name = cafe.name
        else:
            days_worked = (
                (datetime.now(timezone.utc).date() - existing_assignment.start_date).days
                if existing_assignment else 0
            )
            cafe_name = existing_assignment.cafe.name if existing_assignment else None

        updated = self.employee_repo.update(employee)
        employee_response = EmployeeResponse.model_validate({**orm_to_dict(updated), "days_worked": days_worked, "cafe": cafe_name})
        return EmployeeMutationResponse(employee=employee_response, affected_cafes=affected_cafes)

    def delete(self, employee_id: str) -> EmployeeMutationResponse:
        employee = self._get_or_404(employee_id)
        existing_assignment = self.employee_repo.get_assignment(employee_id)

        cafe_id = existing_assignment.cafe_id if existing_assignment else None
        self.employee_repo.delete(employee)

        affected_cafes = []
        if cafe_id:
            count = self.cafe_repo.get_employee_count(cafe_id)
            affected_cafes.append(CafeCountUpdate(id=cafe_id, employees=count))

        return EmployeeMutationResponse(employee=None, affected_cafes=affected_cafes)

    def _get_or_404(self, employee_id: str) -> Employee:
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee", employee_id)
        return employee

    def _get_cafe_or_404(self, cafe_id: str):
        cafe = self.cafe_repo.get_by_id(cafe_id)
        if not cafe:
            raise NotFoundException("Cafe", cafe_id)
        return cafe
