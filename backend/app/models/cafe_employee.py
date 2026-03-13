from datetime import date, datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def _utc_today() -> date:
    return datetime.now(timezone.utc).date()

class CafeEmployee(Base):
    __tablename__ = "cafe_employees"

    # UniqueConstraint on employee_id enforces one-cafe-per-employee at DB level
    __table_args__ = (UniqueConstraint("employee_id", name="uq_employee_one_cafe"),)

    cafe_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("cafes.id", ondelete="CASCADE"), primary_key=True
    )

    employee_id: Mapped[str] = mapped_column(
        String, ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False, default=_utc_today)

    cafe: Mapped["Cafe"] = relationship("Cafe", back_populates="assignments")  # noqa: F821
    employee: Mapped["Employee"] = relationship("Employee", back_populates="assignment")  # noqa: F821
