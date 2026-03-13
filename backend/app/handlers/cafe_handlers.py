from app.commands.cafe_commands import (
    GetCafesQuery,
    CreateCafeCommand,
    UpdateCafeCommand,
    DeleteCafeCommand,
)
from app.services.cafe_service import CafeService
from app.schemas.cafe import CafeCreate, CafeUpdate


class GetCafesHandler:
    def __init__(self, service: CafeService):
        self.service = service

    def handle(self, command: GetCafesQuery):
        return self.service.get_all(command.location)


class CreateCafeHandler:
    def __init__(self, service: CafeService):
        self.service = service

    def handle(self, command: CreateCafeCommand):
        payload = CafeCreate(
            name=command.name,
            description=command.description,
            location=command.location,
        )
        return self.service.create(payload, command.logo)


class UpdateCafeHandler:
    def __init__(self, service: CafeService):
        self.service = service

    def handle(self, command: UpdateCafeCommand):
        payload = CafeUpdate(
            name=command.name,
            description=command.description,
            location=command.location,
        )
        return self.service.update(command.cafe_id, payload, command.logo)


class DeleteCafeHandler:
    def __init__(self, service: CafeService):
        self.service = service

    def handle(self, command: DeleteCafeCommand):
        return self.service.delete(command.cafe_id)