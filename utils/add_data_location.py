import os
import sys
import pandas as pd
from sqlalchemy.orm import Session

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from db.db import SessionLocal
from db.models import LocationModel


def load_data_from_csv():
    db = SessionLocal()
    try:
        # Чтение CSV файла
        df = pd.read_csv("uszips.csv")

        # Преобразование данных в объекты WeatherData
        location_objects = []
        for _, row in df.iterrows():
            location_entry = LocationModel(
                zip=row["zip"],
                lat=row["lat"],
                lng=row["lng"],
                city=row["city"],
                state_name=row["state_name"],
            )
            location_objects.append(location_entry)

        # Вставка данных в базу данных
        db.add_all(location_objects)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    load_data_from_csv()
