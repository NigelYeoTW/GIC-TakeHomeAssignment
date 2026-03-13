from fastapi import APIRouter, Depends, Path, UploadFile, File, Form
from app.schemas.cafe import CafeResponse
from app.mediator import Mediator
from app.dependencies import get_mediator
from app.commands.cafe_commands import GetCafesQuery, CreateCafeCommand, UpdateCafeCommand, DeleteCafeCommand

router = APIRouter(prefix="/cafes", tags=["Cafes"])


@router.get("", response_model=list[CafeResponse])
def get_cafes(
    location: str | None = None,
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(GetCafesQuery(location=location))


@router.post("", response_model=CafeResponse, status_code=201)
def create_cafe(
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    logo: UploadFile | None = File(None),
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(CreateCafeCommand(name=name, description=description, location=location, logo=logo))


@router.put("/{cafe_id}", response_model=CafeResponse)
def update_cafe(
    cafe_id: str = Path(..., pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"),
    name: str | None = Form(None),
    description: str | None = Form(None),
    location: str | None = Form(None),
    logo: UploadFile | None = File(None),
    mediator: Mediator = Depends(get_mediator),
):
    return mediator.send(UpdateCafeCommand(cafe_id=cafe_id, name=name, description=description, location=location, logo=logo))


@router.delete("/{cafe_id}", status_code=204)
def delete_cafe(
    cafe_id: str = Path(..., pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"),
    mediator: Mediator = Depends(get_mediator),
):
    mediator.send(DeleteCafeCommand(cafe_id=cafe_id))
