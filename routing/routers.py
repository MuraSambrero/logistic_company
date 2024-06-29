from fastapi import APIRouter, Depends, Path, Body
from schemas.car import CarSchemaPatch, CarSchema
from schemas.cargo import (
    CargoSchemaAdd,
    CargoSchemaNearCar,
    CargoSchemaWithCars,
    CargoSchemaPatchAPI
)
from services.cargo import CargoService
from services.car import CarService
from depends import get_cargo_service, get_car_service
from fastapi import HTTPException

router_cargo = APIRouter()
router_cars = APIRouter()

# - Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
# - Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
# - Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
# - Редактирование машины по ID (локация (определяется по введенному zip-коду));
# - Редактирование груза по ID (вес, описание);
# - Удаление груза по ID.


@router_cargo.post("/create")
async def create_cargo(
    cargo_schema: CargoSchemaAdd = Body(
        description="JSON с данными для создания груза",
        example={
            "pickup_zip": 1234,
            "delivery_zip": 5678,
            "weight": 500,
            "description": "Fragile item",
        },
    ),
    cargo_service: CargoService = Depends(get_cargo_service),
):
    cargo = cargo_service.create(cargo_schema)
    if cargo is None:
        raise HTTPException(
            status_code=400, detail="Pickup or delivery location not found"
        )
    return cargo


@router_cargo.get("/list")
async def list_cargo(
    cargo_service: CargoService = Depends(get_cargo_service),
) -> list[CargoSchemaNearCar]:
    return cargo_service.get_cargos()


@router_cargo.get(
    "/{cargo_id:int}",
    response_model=CargoSchemaWithCars,
    description="Возвращает груз со списком номеров авто и расстоянием до авто.",
)
async def get_cargo_with_cars(
    cargo_id: int = Path(
        description="ID груза",
        gt=0,
        example=1,
        title="ID",
    ),
    cargo_service: CargoService = Depends(get_cargo_service),
) -> CargoSchemaWithCars:
    cargo = cargo_service.get_cargo_with_cars(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router_cars.patch(
    "/{car_id:str}",
    response_model=CarSchema,
    description="Позволяет изменить данные по авто",
)
async def update_car(
    car_id: str = Path(
        description="Номер машины",
        regex=r"\d{4}[A-Z]",
        title="Автознак",
    ),
    car_data: CarSchemaPatch = Body(
        description="JSON с данными для изменения",
        example={"location_zip": 1234, "capacity": 948},
    ),
    car_service: CarService = Depends(get_car_service),
):
    car = car_service.update_car(car_id, car_data)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router_cargo.patch("{cargo_id:int}")
def update_cargo(
    cargo_id: int = Path(
        description="ID груза",
        gt=0,
        example=1,
        title="ID",
    ),
    cargo_schema: CargoSchemaPatchAPI = Body(
        description="JSON с данными для изменения груза",
        example={
            "pickup_zip": 1234,
            "delivery_zip": 5678,
            "weight": 500,
            "description": "Fragile item",
        },
    ),
    cargo_service: CargoService = Depends(get_cargo_service),
):
    cargo = cargo_service.update_cargo(cargo_id, cargo_schema)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router_cargo.delete("/{cargo_id:int}")
def delete_cargo(
    cargo_id: int = Path(
        description="ID груза",
        gt=0,
        example=1,
        title="ID",
    ),
    cargo_service: CargoService = Depends(get_cargo_service),
):
    cargo = cargo_service.delete_cargo(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo