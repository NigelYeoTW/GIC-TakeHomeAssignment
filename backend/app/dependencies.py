from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.repositories.interfaces import CafeRepositoryInterface, EmployeeRepositoryInterface
from app.repositories.cafe_repository import CafeRepository
from app.repositories.employee_repository import EmployeeRepository
from app.services.cafe_service import CafeService
from app.services.employee_service import EmployeeService
from app.mediator import Mediator
from app.behaviours.logging_behaviour import LoggingBehaviour
from app.commands.cafe_commands import GetCafesQuery, CreateCafeCommand, UpdateCafeCommand, DeleteCafeCommand
from app.commands.employee_commands import GetEmployeesQuery, CreateEmployeeCommand, UpdateEmployeeCommand, DeleteEmployeeCommand
from app.handlers.cafe_handlers import GetCafesHandler, CreateCafeHandler, UpdateCafeHandler, DeleteCafeHandler
from app.handlers.employee_handlers import GetEmployeesHandler, CreateEmployeeHandler, UpdateEmployeeHandler, DeleteEmployeeHandler


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def get_cafe_repo(db: Session = Depends(get_db)) -> CafeRepositoryInterface:
    return CafeRepository(db)


def get_employee_repo(db: Session = Depends(get_db)) -> EmployeeRepositoryInterface:
    return EmployeeRepository(db)


def get_cafe_service(
    cafe_repo: CafeRepositoryInterface = Depends(get_cafe_repo),
) -> CafeService:
    return CafeService(cafe_repo)


def get_employee_service(
    employee_repo: EmployeeRepositoryInterface = Depends(get_employee_repo),
    cafe_repo: CafeRepositoryInterface = Depends(get_cafe_repo),
) -> EmployeeService:
    return EmployeeService(employee_repo, cafe_repo)


def get_mediator(
    cafe_service: CafeService = Depends(get_cafe_service),
    employee_service: EmployeeService = Depends(get_employee_service),
) -> Mediator:
    mediator = Mediator()

    mediator.register_behaviour(LoggingBehaviour())

    mediator.register_handler(GetCafesQuery, GetCafesHandler(cafe_service))
    mediator.register_handler(CreateCafeCommand, CreateCafeHandler(cafe_service))
    mediator.register_handler(UpdateCafeCommand, UpdateCafeHandler(cafe_service))
    mediator.register_handler(DeleteCafeCommand, DeleteCafeHandler(cafe_service))

    mediator.register_handler(GetEmployeesQuery, GetEmployeesHandler(employee_service))
    mediator.register_handler(CreateEmployeeCommand, CreateEmployeeHandler(employee_service))
    mediator.register_handler(UpdateEmployeeCommand, UpdateEmployeeHandler(employee_service))
    mediator.register_handler(DeleteEmployeeCommand, DeleteEmployeeHandler(employee_service))

    return mediator
