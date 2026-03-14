from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.cafe import Cafe
from app.models.cafe_employee import CafeEmployee
from app.repositories.interfaces import CafeRepositoryInterface
from app.utils.logger import get_logger
from app.utils.exceptions import ConflictException, DatabaseException

logger = get_logger(__name__)


class CafeRepository(CafeRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, location: str | None) -> list[tuple[Cafe, int]]:
        try:
            query = (
                self.db.query(Cafe, func.count(CafeEmployee.employee_id).label("employee_count"))
                .outerjoin(CafeEmployee, Cafe.id == CafeEmployee.cafe_id)
                .group_by(Cafe.id)
                .order_by(func.count(CafeEmployee.employee_id).desc())
            )
            if location:
                escaped = location.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
                query = query.filter(Cafe.location.ilike(f"%{escaped}%", escape="\\"))
            return query.all()
        except SQLAlchemyError as e:
            logger.error("cafe.get_all.failed", error=str(e), location=location)
            raise DatabaseException()

    def get_by_id(self, cafe_id: str) -> Cafe | None:
        try:
            return self.db.query(Cafe).filter(Cafe.id == cafe_id).first()
        except SQLAlchemyError as e:
            logger.error("cafe.get_by_id.failed", error=str(e), cafe_id=cafe_id)
            raise DatabaseException()

    def get_employee_count(self, cafe_id: str) -> int:
        try:
            return (
                self.db.query(func.count(CafeEmployee.employee_id))
                .filter(CafeEmployee.cafe_id == cafe_id)
                .scalar() or 0
            )
        except SQLAlchemyError as e:
            logger.error("cafe.get_employee_count.failed", error=str(e), cafe_id=cafe_id)
            raise DatabaseException()

    def create(self, cafe: Cafe) -> Cafe:
        try:
            self.db.add(cafe)
            self.db.commit()
            self.db.refresh(cafe)
            logger.info("cafe.created", cafe_id=cafe.id, name=cafe.name)
            return cafe
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("cafe.create.conflict", error=str(e), name=cafe.name)
            raise ConflictException("A cafe with these details already exists")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("cafe.create.failed", error=str(e), name=cafe.name)
            raise DatabaseException()

    def update(self, cafe: Cafe) -> Cafe:
        try:
            self.db.commit()
            self.db.refresh(cafe)
            logger.info("cafe.updated", cafe_id=cafe.id)
            return cafe
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("cafe.update.conflict", error=str(e), cafe_id=cafe.id)
            raise ConflictException("Update conflicts with existing data")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("cafe.update.failed", error=str(e), cafe_id=cafe.id)
            raise DatabaseException()

    def delete(self, cafe: Cafe) -> None:
        try:
            self.db.delete(cafe)
            self.db.commit()
            logger.info("cafe.deleted", cafe_id=cafe.id)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("cafe.delete.failed", error=str(e), cafe_id=cafe.id)
            raise DatabaseException()

    def delete_with_employees(self, cafe: Cafe) -> None:
        from app.models.employee import Employee
        try:
            subquery = self.db.query(CafeEmployee.employee_id).filter(CafeEmployee.cafe_id == cafe.id).subquery()
            self.db.query(Employee).filter(Employee.id.in_(subquery)).delete(synchronize_session=False)
            self.db.delete(cafe)
            self.db.commit()
            logger.info("cafe.deleted_with_employees", cafe_id=cafe.id)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("cafe.delete_with_employees.failed", error=str(e), cafe_id=cafe.id)
            raise DatabaseException()
