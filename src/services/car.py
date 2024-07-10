from schemas.car import CarSchemaPatch, CarSchema, CarSchemaRel
from repositories.car import CarRepository


class CarService:
    def __init__(self, car_repository: CarRepository):
        self.repository = car_repository

    def update_car(
        self,
        car_id: str,
        car_data: CarSchemaPatch,
    ) -> CarSchema | None:
        car = self.repository.update_car(
            car_id=car_id,
            car_data=car_data,
        )
        return car

    def get_cars_rel(self) -> list[CarSchemaRel]:
        return self.repository.get_cars_rel()
