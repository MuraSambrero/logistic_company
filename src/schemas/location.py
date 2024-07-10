from pydantic import BaseModel


class LocationSchema(BaseModel):
    zip: int
    city: str
    state_name: str
    lat: float
    lng: float


class LocationSchemaCsv(LocationSchema):
    pass


class LocationSchemaAddDTO(LocationSchema):

    def __hash__(self):
        return hash(self.zip)
