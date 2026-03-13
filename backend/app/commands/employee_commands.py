from dataclasses import dataclass


@dataclass
class GetEmployeesQuery:
    cafe: str | None = None


@dataclass
class CreateEmployeeCommand:
    name: str
    email_address: str
    phone_number: str
    gender: str
    cafe_id: str | None = None


@dataclass
class UpdateEmployeeCommand:
    employee_id: str
    name: str | None = None
    email_address: str | None = None
    phone_number: str | None = None
    gender: str | None = None
    cafe_id: str | None = None


@dataclass
class DeleteEmployeeCommand:
    employee_id: str
