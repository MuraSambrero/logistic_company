from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy import ForeignKey


# # - Локация должна содержать в себе следующие характеристики:
# #     - город;
# #     - штат;
# #     - почтовый индекс (zip);
# #     - широта;
# #     - долгота.


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


# # - Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
# # - Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
# # - Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
# # - Редактирование машины по ID (локация (определяется по введенному zip-коду));
# # - Редактирование груза по ID (вес, описание);
# # - Удаление груза по ID.

# # - Груз обязательно должен содержать следующие характеристики:
# #     - локация pick-up;
# #     - локация delivery;
# #     - вес (1-1000);
# #     - описание.


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


# # - Редактирование машины по ID (локация (определяется по введенному zip-коду));


# # - Машина обязательно должна в себя включать следующие характеристики:
# #     - уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце, пример: "1234A", "2534B", "9999Z")
# #     - текущая локация;
# #     - грузоподъемность (1-1000).


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
