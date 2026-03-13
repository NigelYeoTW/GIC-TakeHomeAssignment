import random
import string
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, Integer
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.employee import Employee
from app.models.cafe_employee import CafeEmployee
from app.models.cafe import Cafe
from app.repositories.interfaces import EmployeeRepositoryInterface
from app.utils.logger import get_logger
from app.utils.exceptions import ConflictException, DatabaseException

logger = get_logger(__name__)


class EmployeeRepository(EmployeeRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, cafe_name: str | None) -> list[tuple[Employee, int, str | None]]:
        try:
            days_worked = func.coalesce(
                func.extract("day", func.now() - CafeEmployee.start_date).cast(Integer), 0
            ).label("days_worked")

            query = (
                self.db.query(Employee, days_worked, Cafe.name.label("cafe_name"))
                .outerjoin(CafeEmployee, Employee.id == CafeEmployee.employee_id)
                .outerjoin(Cafe, CafeEmployee.cafe_id == Cafe.id)
                .order_by(days_worked.desc())
            )
            if cafe_name:
                escaped = cafe_name.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
                query = query.filter(Cafe.name.ilike(f"%{escaped}%", escape="\\"))
            return query.all()
        except SQLAlchemyError as e:
            logger.error("employee.get_all.failed", error=str(e), cafe_name=cafe_name)
            raise DatabaseException()

    def get_by_id(self, employee_id: str) -> Employee | None:
        try:
            return self.db.query(Employee).filter(Employee.id == employee_id).first()
        except SQLAlchemyError as e:
            logger.error("employee.get_by_id.failed", error=str(e), employee_id=employee_id)
            raise DatabaseException()

    def get_assignment(self, employee_id: str) -> CafeEmployee | None:
        try:
            return (
                self.db.query(CafeEmployee)
                .options(joinedload(CafeEmployee.cafe))
                .filter(CafeEmployee.employee_id == employee_id)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error("employee.get_assignment.failed", error=str(e), employee_id=employee_id)
            raise DatabaseException()

    @staticmethod
    def _generate_employee_id() -> str:
        chars = string.ascii_uppercase + string.digits
        suffix = "".join(random.choices(chars, k=7))
        return f"UI{suffix}"

    def create_with_optional_assignment(self, employee: Employee, cafe_id: str | None) -> Employee:
        for attempt in range(5):
            try:
                employee.id = self._generate_employee_id()
                self.db.add(employee)
                self.db.flush()
                if cafe_id:
                    self.db.add(CafeEmployee(
                        employee_id=employee.id,
                        cafe_id=cafe_id,
                        start_date=datetime.now(timezone.utc).date(),
                    ))
                self.db.commit()
                self.db.refresh(employee)
                logger.info("employee.created", employee_id=employee.id, name=employee.name)
                return employee
            except IntegrityError as e:
                self.db.rollback()
                error_str = str(e).lower()
                if "email" in error_str:
                    logger.warning("employee.create.email_conflict", email=employee.email_address)
                    raise ConflictException("An employee with this email already exists")
                logger.warning("employee.id_collision", attempt=attempt + 1, employee_id=employee.id)
            except SQLAlchemyError as e:
                self.db.rollback()
                logger.error("employee.create.failed", error=str(e))
                raise DatabaseException()
        logger.error("employee.id_generation.exhausted")
        raise DatabaseException()

    def reassign_cafe(self, old_assignment: CafeEmployee | None, employee_id: str, new_cafe_id: str) -> None:
        try:
            if old_assignment:
                self.db.delete(old_assignment)
                self.db.flush()
            self.db.add(CafeEmployee(
                employee_id=employee_id,
                cafe_id=new_cafe_id,
                start_date=datetime.now(timezone.utc).date(),
            ))
            self.db.commit()
            logger.info("employee.reassigned", employee_id=employee_id, new_cafe_id=new_cafe_id)
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("employee.reassign.conflict", error=str(e), employee_id=employee_id)
            raise ConflictException("Assignment conflicts with existing data")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("employee.reassign.failed", error=str(e), employee_id=employee_id)
            raise DatabaseException()

    def update(self, employee: Employee) -> Employee:
        try:
            self.db.commit()
            self.db.refresh(employee)
            logger.info("employee.updated", employee_id=employee.id)
            return employee
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("employee.update.conflict", error=str(e), employee_id=employee.id)
            raise ConflictException("Update conflicts with existing data")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("employee.update.failed", error=str(e), employee_id=employee.id)
            raise DatabaseException()

    def delete(self, employee: Employee) -> None:
        try:
            self.db.delete(employee)
            self.db.commit()
            logger.info("employee.deleted", employee_id=employee.id)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("employee.delete.failed", error=str(e), employee_id=employee.id)
            raise DatabaseException()
