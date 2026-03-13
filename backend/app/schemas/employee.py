import re
from pydantic import BaseModel, Field, field_validator, EmailStr


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=6, max_length=10)
    email_address: EmailStr
    phone_number: str
    gender: str = Field(..., pattern="^(Male|Female)$")

    @field_validator("phone_number")
    @classmethod
    def validate_sg_phone(cls, v: str) -> str:
        if not re.match(r"^[89]\d{7}$", v):
            raise ValueError("Phone number must start with 8 or 9 and be exactly 8 digits")
        return v


class EmployeeCreate(EmployeeBase):
    cafe_id: str | None = None


class EmployeeUpdate(BaseModel):
    name: str | None = Field(None, min_length=6, max_length=10)
    email_address: EmailStr | None = None
    phone_number: str | None = None
    gender: str | None = Field(None, pattern="^(Male|Female)$")
    cafe_id: str | None = None  # None = unassign, provided = reassign

    @field_validator("phone_number")
    @classmethod
    def validate_sg_phone(cls, v: str | None) -> str | None:
        if v is not None and not re.match(r"^[89]\d{7}$", v):
            raise ValueError("Phone number must start with 8 or 9 and be exactly 8 digits")
        return v


class EmployeeResponse(EmployeeBase):
    id: str
    days_worked: int   # derived: (today - start_date).days
    cafe: str | None

    model_config = {"from_attributes": True}


class CafeCountUpdate(BaseModel):
    id: str
    employees: int


class EmployeeMutationResponse(BaseModel):
    employee: EmployeeResponse | None       # None on delete
    affected_cafes: list[CafeCountUpdate]   # cafes whose counts changed
