from pydantic import BaseModel, Field
from .location import LocationSchema
from .car import CarsWithDistance


class CargoSchemaAdd(BaseModel):
    pickup_zip: int
    delivery_zip: int
    weight: int = Field(gt=0, lt=1001)
    description: str


class CargoSchema(CargoSchemaAdd):
    id: int


class CargoSchemaPickup(CargoSchema):
    pickup_location: LocationSchema


class CargoSchemaNearCar(CargoSchemaAdd):
    count_car: int = 0


class CargoSchemaWithCars(CargoSchemaAdd):
    cars: list[CarsWithDistance] | None = None

class CargoSchemaPatchAPI(BaseModel):
    pickup_zip: int | None = None
    delivery_zip: int | None = None
    description: str | None = None
    weight: int | None = Field(default=None, gt=0, lt=1001)

class CargoSchemaPatch(CargoSchemaPatchAPI):
    id: int
