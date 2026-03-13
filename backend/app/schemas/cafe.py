from pydantic import BaseModel, Field


class CafeBase(BaseModel):
    name: str = Field(..., min_length=6, max_length=10)
    description: str = Field(..., max_length=256)
    location: str = Field(..., min_length=1, max_length=255)


class CafeCreate(CafeBase):
    pass


class CafeUpdate(BaseModel):
    name: str | None = Field(None, min_length=6, max_length=10)
    description: str | None = Field(None, max_length=256)
    location: str | None = Field(None, min_length=1, max_length=255)
    logo: str | None = None


class CafeResponse(CafeBase):
    id: str
    logo: str | None
    employees: int 

    model_config = {"from_attributes": True}
