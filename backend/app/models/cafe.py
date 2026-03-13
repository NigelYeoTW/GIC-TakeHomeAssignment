import uuid
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Cafe(Base):
    __tablename__ = "cafes"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    logo: Mapped[str | None] = mapped_column(String(512), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)

    assignments: Mapped[list["CafeEmployee"]] = relationship(  # noqa: F821
        "CafeEmployee", back_populates="cafe", cascade="all, delete-orphan"
    )
