from sqlalchemy import insert
from db.models import CargoModel
from schemas.cargo import (
    CargoSchemaPickup,
    CargoSchemaAdd,
    CargoSchema,
    CargoSchemaPatch,
)
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from repositories.repository import Repository
from sqlalchemy import update


class CargoRepository(Repository):
    def create(self, cargo_schema: CargoSchemaAdd) -> CargoSchema | None:
        query = (
            insert(CargoModel)
            .values(cargo_schema.model_dump(exclude_none=True))
            .returning(CargoModel)
        )
        try:
            cursor = self.get_new_session.execute(query)
        except IntegrityError:
            return None
        cargo_model = cursor.scalar_one_or_none()
        if cargo_model is None:
            return None
        cargo_dto = CargoSchema.model_validate(cargo_model, from_attributes=True)
        return cargo_dto

    def get_cargos_pickup_location(
        self, min_weight: int, max_weight: int
    ) -> list[CargoSchemaPickup]:
        query = (
            select(CargoModel)
            .select_from(CargoModel)
            .where(
                CargoModel.weight >= min_weight,
                CargoModel.weight <= max_weight,
            )
            .options(selectinload(CargoModel.pickup_location))
        )
        cursor = self.get_new_session.execute(query)
        cargos = cursor.scalars().all()
        cargos_DTO = [
            CargoSchemaPickup.model_validate(row, from_attributes=True)
            for row in cargos
        ]
        return cargos_DTO

    def get_cargo(self, cargo_id: int) -> CargoSchemaPickup | None:
        query = (
            select(CargoModel)
            .select_from(CargoModel)
            .where(CargoModel.id == cargo_id)
            .options(selectinload(CargoModel.pickup_location))
        )
        cursor = self.get_new_session.execute(query)
        cargo_with_location = cursor.scalar_one_or_none()
        if cargo_with_location is None:
            return None
        return CargoSchemaPickup.model_validate(
            cargo_with_location, from_attributes=True
        )

    def update_cargo(self, cargo_schema: CargoSchemaPatch) -> CargoSchema | None:
        query = (
            update(CargoModel)
            .where(CargoModel.id == cargo_schema.id)
            .values(cargo_schema.model_dump(exclude_none=True))
            .returning(CargoModel)
        )
        try:
            cursor = self.get_new_session.execute(query)
        except IntegrityError:
            return None
        cargo_model = cursor.scalar_one_or_none()
        if cargo_model is None:
            return None
        cargo_dto = CargoSchema.model_validate(cargo_model, from_attributes=True)
        return cargo_dto

    def delete_cargo(self, cargo_id: int) -> CargoSchema | None:
        session = self.get_session()
        stmt = delete(CargoModel).where(CargoModel.id == cargo_id).returning(CargoModel)
        cursor = session.execute(stmt)
        cargo_model = cursor.scalar_one_or_none()
        if cargo_model is None:
            return None
        cargo_dto = CargoSchema.model_validate(cargo_model, from_attributes=True)
        return cargo_dto

    def clear_table(self):
        session = self.get_session()
        session.query(CargoModel).delete()
        session.commit()
