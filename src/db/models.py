from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy import ForeignKey


class LocationModel(Base):
    __tablename__ = "location"

    zip = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    state_name = Column(String)
    lat = Column(String)
    lng = Column(String)

    cargo_pickup = relationship(
        "CargoModel",
        back_populates="pickup_location",
        foreign_keys="CargoModel.pickup_zip",
    )
    cargo_delivery = relationship(
        "CargoModel",
        back_populates="delivery_location",
        foreign_keys="CargoModel.delivery_zip",
    )
    cars = relationship("CarModel", back_populates="location")


class CargoModel(Base):
    __tablename__ = "cargo"

    id = Column(Integer, primary_key=True, index=True)
    pickup_zip = Column(Integer, ForeignKey("location.zip"))
    delivery_zip = Column(Integer, ForeignKey("location.zip"))
    weight = Column(Integer)
    description = Column(String)

    pickup_location = relationship(
        "LocationModel",
        back_populates="cargo_pickup",
        foreign_keys="CargoModel.pickup_zip",
    )

    delivery_location = relationship(
        "LocationModel",
        back_populates="cargo_delivery",
        foreign_keys="CargoModel.delivery_zip",
    )


class CarModel(Base):
    __tablename__ = "car"

    id = Column(String, primary_key=True, index=True)
    capacity = Column(Integer)
    location_zip = Column(Integer, ForeignKey("location.zip"))

    location = relationship(
        "LocationModel",
        back_populates="cars",
        foreign_keys="CarModel.location_zip",
    )
