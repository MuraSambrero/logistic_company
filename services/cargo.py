from repositories.cargo import CargoRepository
from schemas.cargo import (
    CargoSchema,
    CargoSchemaAdd,
    CargoSchemaNearCar,
    CargoSchemaWithCars,
    CargoSchemaPatchAPI,
    CargoSchemaPatch,
)
from schemas.car import CarsWithDistance
from services.location import LocationService
from services.car import CarService


class CargoService:
    def __init__(
        self,
        cargo_repository: CargoRepository,
        location_service: LocationService,
        car_service: CarService,
    ):
        self.repository = cargo_repository
        self.location_service = location_service
        self.car_service = car_service

    def create(self, cargo_schema: CargoSchemaAdd):
        result = self.repository.create(cargo_schema)
        return result

    def get_cargos(self) -> list[CargoSchemaNearCar]:
        cargos_pickup = self.repository.get_cargos_pickup_location()
        cars_with_locations = self.car_service.get_cars_rel()
        cargo_near_cars: list[CargoSchemaNearCar] = []
        for cargo in cargos_pickup:
            new_car = CargoSchemaNearCar.model_validate(cargo, from_attributes=True)
            cargo_near_cars.append(new_car)
            for car in cars_with_locations:
                distance = LocationService.get_distance(
                    cargo.pickup_location, car.location
                )
                if distance <= 450:
                    new_car.count_car += 1
        return cargo_near_cars

    def get_cargo_with_cars(self, cargo_id: int) -> CargoSchemaWithCars | None:
        cargo_with_location = self.repository.get_cargo(cargo_id)
        if cargo_with_location is None:
            return None
        cars_with_locations = self.car_service.get_cars_rel()
        cargo = CargoSchemaWithCars.model_validate(
            cargo_with_location, from_attributes=True
        )
        cargo.cars = []
        for car in cars_with_locations:
            distance = LocationService.get_distance(
                cargo_with_location.pickup_location, car.location
            )
            car = CarsWithDistance.model_validate(car, from_attributes=True)
            car.distance = distance
            cargo.cars.append(car)
        return cargo

    def update_cargo(
        self, cargo_id: int, cargo_schema: CargoSchemaPatchAPI
    ) -> CargoSchema | None:
        cargo = CargoSchemaPatch(id=cargo_id, **cargo_schema.model_dump(exclude_none=True))
        result = self.repository.update_cargo(cargo)
        return result

    def delete_cargo(self, cargo_id: int) -> CargoSchema | None:
        cargo = self.repository.delete_cargo(cargo_id)
        return cargo