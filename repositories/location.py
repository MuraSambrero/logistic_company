from db.models import LocationModel
from schemas.location import LocationSchema
from repositories.repository import Repository

class LocationRepository(Repository):

    def get(self, location_zip: int) -> LocationSchema | None:
        '''
        Get location by zip code

        :param location_zip: int
        :param db: SessionLocal()
        :return: LocationModel object
        :raise exceptions_404.LocationNotFoundException: 
        if location not found in database.
        '''
        location = self.session.query(LocationModel).get(location_zip)
        if location is None:
            return None
        location_schema = LocationSchema.model_validate(location, from_attributes=True)
        return location_schema
    
    def get_object_coords(self, location_zip: int):
        '''
        Get location by zip code

        :param location_zip: int
        :param db: SessionLocal()
        :return: LocationModel object
        :raise exceptions_404.LocationNotFoundException:
        if location not found in database.
        '''
        location = self.get(location_zip)
        return (location.lat, location.lng)
    
    def get_all(self) -> list[LocationSchema]:
        locations = self.session.query(LocationModel).all()
        locations_DTO = [LocationSchema.model_validate(row, from_attributes=True) for row in locations]
        return locations_DTO