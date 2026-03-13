from dataclasses import dataclass
from fastapi import UploadFile


@dataclass
class GetCafesQuery:
    location: str | None = None


@dataclass
class CreateCafeCommand:
    name: str
    description: str
    location: str
    logo: UploadFile | None = None


@dataclass
class UpdateCafeCommand:
    cafe_id: str
    name: str | None = None
    description: str | None = None
    location: str | None = None
    logo: UploadFile | None = None


@dataclass
class DeleteCafeCommand:
    cafe_id: str
