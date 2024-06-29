from schemas.location import LocationSchema
from geopy.distance import geodesic as GD
from repositories.location import LocationRepository


class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    def get(self, location_zip: int) -> LocationSchema | None:
        return self.repository.get(location_zip)

    @staticmethod
    def get_coord(location: LocationSchema) -> tuple[float, float]:
        return float(location.lat), float(location.lng)

    @classmethod
    def get_distance(
        cls,
        location_first: LocationSchema,
        location_second: LocationSchema,
    ) -> float:
        distance = GD(
            cls.get_coord(location_first),
            cls.get_coord(location_second),
        ).miles
        return distance