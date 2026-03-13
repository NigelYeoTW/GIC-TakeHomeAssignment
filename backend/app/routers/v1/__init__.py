from fastapi import APIRouter
from app.routers.v1 import cafes, employees

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(cafes.router)
v1_router.include_router(employees.router)
