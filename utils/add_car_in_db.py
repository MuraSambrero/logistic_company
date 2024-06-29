import pandas as pd
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

import random
import string
from db.db import SessionLocal
from db.models import CarModel, LocationModel


def number_car():
    string_number = "".join(list(string.printable)[:10])
    digits = random.sample(string_number, 4)
    alphabet = random.sample(string.ascii_uppercase, 1)
    number = "".join(digits) + "".join(alphabet)
    return number


def extract_locations_and_load_car():
    db = SessionLocal()
    df = pd.DataFrame(
        data=[],
        columns=["id", "capacity", "location_zip"],
    )

    query = db.query(LocationModel, LocationModel.zip).all()
    for i in range(20):
        row_data = {
            "id": number_car(),
            "location_zip": random.choice(query)[1],
            "capacity": random.randint(1, 1001),
        }
        df_to_add = pd.DataFrame([row_data])
        df = pd.concat([df, df_to_add], ignore_index=True)

    car_objects = []
    for _, row in df.iterrows():
        car_entry = CarModel(
            id=row["id"],
            capacity=row["capacity"],
            location_zip=row["location_zip"],
        )
        car_objects.append(car_entry)

    db.add_all(car_objects)
    db.commit()
    db.close()


if __name__ == "__main__":
    extract_locations_and_load_car()
