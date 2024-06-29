from pydantic import BaseModel
from .location import LocationSchema

# - Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
# - Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
# - Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
# - Редактирование груза по ID (вес, описание);
# - Удаление груза по ID.

# - Груз обязательно должен содержать следующие характеристики:
#     - локация pick-up;
#     - локация delivery;
#     - вес (1-1000);
#     - описание.


# - Редактирование машины по ID (локация (определяется по введенному zip-коду));


class CarSchemaAdd(BaseModel):
    id: str
    location_zip: int
    capacity: int

class CarSchema(CarSchemaAdd):
    pass

class CarSchemaRel(CarSchemaAdd):
    location: LocationSchema

class CarsWithDistance(BaseModel):
    id: str
    distance: float | None = None

class CarSchemaPatch(BaseModel):
    id: str | None = None
    location_zip: int | None  = None
    capacity: int | None  = None