from app.commands.employee_commands import (
    GetEmployeesQuery,
    CreateEmployeeCommand,
    UpdateEmployeeCommand,
    DeleteEmployeeCommand,
)
from app.services.employee_service import EmployeeService
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class GetEmployeesHandler:
    def __init__(self, service: EmployeeService):
        self.service = service

    def handle(self, command: GetEmployeesQuery):
        return self.service.get_all(command.cafe)


class CreateEmployeeHandler:
    def __init__(self, service: EmployeeService):
        self.service = service

    def handle(self, command: CreateEmployeeCommand):
        payload = EmployeeCreate(
            name=command.name,
            email_address=command.email_address,
            phone_number=command.phone_number,
            gender=command.gender,
            cafe_id=command.cafe_id,
        )
        return self.service.create(payload)


class UpdateEmployeeHandler:
    def __init__(self, service: EmployeeService):
        self.service = service

    def handle(self, command: UpdateEmployeeCommand):
        payload = EmployeeUpdate(
            name=command.name,
            email_address=command.email_address,
            phone_number=command.phone_number,
            gender=command.gender,
            cafe_id=command.cafe_id,
        )
        return self.service.update(command.employee_id, payload)


class DeleteEmployeeHandler:
    def __init__(self, service: EmployeeService):
        self.service = service

    def handle(self, command: DeleteEmployeeCommand):
        return self.service.delete(command.employee_id)