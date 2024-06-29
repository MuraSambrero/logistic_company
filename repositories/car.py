from sqlalchemy.orm import selectinload
from schemas.car import CarSchema, CarSchemaRel, CarSchemaPatch
from db.models import CarModel
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from repositories.repository import Repository


class CarRepository(Repository):
    def get_cars(self) -> list[CarSchema]:
        cars = self.get_new_session.query(CarModel).all()
        cars_DTO = [CarSchema.model_validate(row, from_attributes=True) for row in cars]
        return cars_DTO

    def get_cars_rel(self) -> list[CarSchemaRel]:
        query = (
            select(CarModel)
            .select_from(CarModel)
            .options(selectinload(CarModel.location))
        )
        cars = self.get_new_session.execute(query)
        cars = cars.scalars().all()
        cars_DTO = [
            CarSchemaRel.model_validate(row, from_attributes=True) for row in cars
        ]
        return cars_DTO

    def update_car(
        self,
        car_id: str,
        car_data: CarSchemaPatch,
    ) -> CarSchema | None:
        stmt = (
            update(CarModel)
            .where(CarModel.id == car_id)
            .values(car_data.model_dump(exclude_none=True))
            .returning(CarModel)
        )
        try:
            car = self.get_new_session.execute(stmt).scalar_one_or_none()
        except IntegrityError:
            return None
        car_DTO = CarSchema.model_validate(car, from_attributes=True) if car else None
        return car_DTO
