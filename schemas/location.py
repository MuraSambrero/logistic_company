from pydantic import BaseModel


class LocationSchema(BaseModel):
    zip: int
    city: str
    state_name: str
    lat: float
    lng: float