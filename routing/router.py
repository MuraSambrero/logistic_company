from fastapi import APIRouter
from .routers import router_cargo, router_cars

router = APIRouter()

router.include_router(router_cargo, prefix="/cargo", tags=["cargo"])
router.include_router(router_cars, prefix="/cars", tags=["cars"])