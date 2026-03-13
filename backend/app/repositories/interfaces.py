from abc import ABC, abstractmethod
from app.models.cafe import Cafe
from app.models.employee import Employee
from app.models.cafe_employee import CafeEmployee


class CafeRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self, location: str | None) -> list[tuple[Cafe, int]]:
        ...

    @abstractmethod
    def get_by_id(self, cafe_id: str) -> Cafe | None:
        ...

    @abstractmethod
    def get_employee_count(self, cafe_id: str) -> int:
        ...

    @abstractmethod
    def create(self, cafe: Cafe) -> Cafe:
        ...

    @abstractmethod
    def update(self, cafe: Cafe) -> Cafe:
        ...

    @abstractmethod
    def delete(self, cafe: Cafe) -> None:
        ...


class EmployeeRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self, cafe_name: str | None) -> list[tuple[Employee, int, str | None]]:
        ...

    @abstractmethod
    def get_by_id(self, employee_id: str) -> Employee | None:
        ...

    @abstractmethod
    def get_assignment(self, employee_id: str) -> CafeEmployee | None:
        ...

    @abstractmethod
    def create_with_optional_assignment(self, employee: Employee, cafe_id: str | None) -> Employee:
        ...

    @abstractmethod
    def reassign_cafe(self, old_assignment: CafeEmployee | None, employee_id: str, new_cafe_id: str) -> None:
        ...

    @abstractmethod
    def update(self, employee: Employee) -> Employee:
        ...

    @abstractmethod
    def delete(self, employee: Employee) -> None:
        ...
