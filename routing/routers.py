from fastapi import APIRouter, Depends, Path, Body
from schemas.car import CarSchemaPatch, CarSchema
from schemas.cargo import (
    CargoSchemaAdd,
    CargoSchemaNearCar,
    CargoSchemaWithCars,
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
    cargo_schema: CargoSchemaAdd,
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
    cargo_id: int = Path(),
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
    car_data: CarSchemaPatch = Body(),
    car_service: CarService = Depends(get_car_service),
):
    car = car_service.update_car(car_id, car_data)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


# @router_cargo.delete("/{id}")
# async def delete_cargo():
#     pass


# @router_cars.get("/")
# async def get_cars(
#     db: Session = Depends(get_db),
# ):
#     return CarService.get_cars_rel(db)


# @router_cars.patch("/{id}")
# async def update_car():
#     pass
