from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)  # UIXXXXXXX
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email_address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(8), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)

    assignment: Mapped["CafeEmployee | None"] = relationship(  # noqa: F821
        "CafeEmployee", back_populates="employee", uselist=False, cascade="all, delete-orphan"
    )
