from fastapi import APIRouter, Depends, Path, Body, Query
from schemas.car import CarSchemaPatch, CarSchema
from schemas.cargo import (
    CargoSchemaAdd,
    CargoSchemaNearCar,
    CargoSchemaWithCars,
    CargoSchemaPatchAPI,
)
from services.cargo import CargoService
from services.car import CarService
from depends import get_cargo_service, get_car_service
from fastapi import HTTPException
from schemas.cargo import CargoSchema

router_cargo = APIRouter()
router_cars = APIRouter()


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
    """
    ### Создание груза.
    ## Arguments:
    - cargo_schema: CargoSchemaAdd - JSON с данными для создания груза.
    - cargo_service: CargoService - Сервис для работы с грузом.
    ## Returns:
    - cargo: CargoSchema - Созданный груз.
    """
    cargo = cargo_service.create(cargo_schema)
    if cargo is None:
        raise HTTPException(
            status_code=400, detail="Pickup or delivery location not found"
        )
    return cargo


@router_cargo.get("/list")
async def list_cargo(
    cargo_service: CargoService = Depends(
        get_cargo_service,
    ),
    min_weight: int = Query(
        ge=1,
        le=1000,
        description="Минимальный вес груза",
        example=1,
        default=1,
    ),
    max_weight: int = Query(
        ge=1,
        le=1000,
        description="Максимальный вес груза",
        example=1000,
        default=1000,
    ),
    max_distance: float = Query(
        ge=0,
        description="Расстояние до авто",
        example=450,
        default=450,
    ),
) -> list[CargoSchemaNearCar]:
    """
    ### Получение списка грузов.
    ## Arguments:
    - cargo_service: CargoService - Сервис для работы с грузом.
    ## Returns:
    - list[CargoSchemaNearCar] - Список грузов.
    """
    return cargo_service.get_cargos(
        min_weight=min_weight,
        max_weight=max_weight,
        max_distance=max_distance,
    )


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
    """
    ### Получение груза с кол-ом машин расстояние до которых < 450 миль.
    ## Arguments:
    - cargo_id: int - ID груза.
    - cargo_service: CargoService - Сервис для работы с грузом.
    ## Returns:
    - CargoSchemaWithCars - Груз с информацией о машинах.
    """
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
) -> CarSchema:
    """
    ### Изменение данных авто.
    ## Arguments:
    - car_id: str - Номер машины.
    - car_data: CarSchemaPatch - JSON с данными для изменения.
    - car_service: CarService - Сервис для работы с автомобилем.
    ## Returns:
    - CarSchema - Измененный автомобиль.
    """
    car = car_service.update_car(car_id, car_data)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router_cargo.patch("{cargo_id:int}")
async def update_cargo(
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
) -> CargoSchema:
    """
    ### Изменение груза.
    ## Arguments:
    - cargo_id: int - ID груза.
    - cargo_schema: CargoSchemaPatchAPI - JSON с данными для изменения груза.
    - cargo_service: CargoService - Сервис для работы с грузом.
    ## Returns:
    - CargoSchema - Измененный груз.
    """
    cargo = cargo_service.update_cargo(cargo_id, cargo_schema)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router_cargo.delete("/{cargo_id:int}")
async def delete_cargo(
    cargo_id: int = Path(
        description="ID груза",
        gt=0,
        example=1,
        title="ID",
    ),
    cargo_service: CargoService = Depends(get_cargo_service),
) -> CargoSchema:
    """
    ### Удаление груза.
    ## Arguments:
    - cargo_id: int - ID груза.
    - cargo_service: CargoService - Сервис для работы с грузом.
    ## Returns:
    - CargoSchema - Удаленный груз.
    """
    cargo = cargo_service.delete_cargo(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


# Вес, мили, ближайшие машины до грузов
