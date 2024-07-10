from db.models import LocationModel
from schemas.location import LocationSchemaAddDTO, LocationSchema
from repositories.repository import Repository
from sqlalchemy import insert


class LocationRepository(Repository):
    def get(self, location_zip: int) -> LocationSchema | None:
        """
        Get location by zip code

        :param location_zip: int
        :param db: SessionLocal()
        :return: LocationModel object
        :raise exceptions_404.LocationNotFoundException:
        if location not found in database.
        """
        location = self.get_new_session.query(LocationModel).get(location_zip)
        if location is None:
            return None
        location_schema = LocationSchema.model_validate(location, from_attributes=True)
        return location_schema

    def get_object_coords(self, location_zip: int):
        """
        Get location by zip code

        :param location_zip: int
        :param db: SessionLocal()
        :return: LocationModel object
        :return None
        if location not found in database.
        """
        location = self.get(location_zip)
        if location is None:
            return None
        return (location.lat, location.lng)

    def get_all(self) -> list[LocationSchema]:
        locations = self.get_new_session.query(LocationModel).all()
        locations_DTO = [
            LocationSchema.model_validate(row, from_attributes=True)
            for row in locations
        ]
        return locations_DTO

    def insert_locations(self, locations: list[LocationSchemaAddDTO]):
        values = [i.model_dump() for i in locations]
        stmt = insert(LocationModel).values(values).returning(LocationModel)
        session = self.get_session()
        cursor = session.execute(stmt)
        session.commit()
        locations = list(cursor.scalars().all())
        locations_DTO = [
            LocationSchema.model_validate(row, from_attributes=True)
            for row in locations
        ]
        return locations_DTO


    
