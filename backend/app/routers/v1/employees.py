from fastapi import APIRouter, Depends, Path
from app.schemas.employee import EmployeeResponse, EmployeeMutationResponse
from app.mediator import Mediator
from app.dependencies import get_mediator
from app.commands.employee_commands import GetEmployeesQuery, CreateEmployeeCommand, UpdateEmployeeCommand, DeleteEmployeeCommand
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=list[EmployeeResponse])
def get_employees(
    cafe: str | None = None,
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(GetEmployeesQuery(cafe=cafe))


@router.post("", response_model=EmployeeMutationResponse, status_code=201)
def create_employee(
    payload: EmployeeCreate,
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(CreateEmployeeCommand(
        name=payload.name,
        email_address=payload.email_address,
        phone_number=payload.phone_number,
        gender=payload.gender,
        cafe_id=payload.cafe_id,
    ))


@router.put("/{employee_id}", response_model=EmployeeMutationResponse)
def update_employee(
    employee_id: str = Path(..., pattern=r"^UI[A-Z0-9]{7}$"),
    payload: EmployeeUpdate = ...,
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(UpdateEmployeeCommand(
        employee_id=employee_id,
        name=payload.name,
        email_address=payload.email_address,
        phone_number=payload.phone_number,
        gender=payload.gender,
        cafe_id=payload.cafe_id,
    ))


@router.delete("/{employee_id}", response_model=EmployeeMutationResponse)
def delete_employee(
    employee_id: str = Path(..., pattern=r"^UI[A-Z0-9]{7}$"),
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(DeleteEmployeeCommand(employee_id=employee_id))
