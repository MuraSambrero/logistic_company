from geopy.distance import geodesic as GD
from repositories.location import LocationRepository
import pandas as pd
from schemas.location import LocationSchemaCsv, LocationSchemaAddDTO, LocationSchema


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

    def load_locations_from_csv(self, filename: str) -> list[LocationSchema]:
        df: pd.DataFrame = pd.read_csv(filename)
        df_dicts = df.to_dict(orient="records")

        locations: list[LocationSchemaCsv] = [LocationSchemaCsv(**i) for i in df_dicts]
        locations_dto = [
            LocationSchemaAddDTO.model_validate(i, from_attributes=True)
            for i in locations
        ]
        locations_DTO = self.repository.insert_locations(locations=locations_dto)
        return locations_DTO
