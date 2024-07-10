import pytest
from .depends_test import (
    location_service,
    car_repository,
    cargo_repository,
    repository
)

@pytest.fixture(scope="session", autouse=True)
def init_db():
    repository.drop_tables()
    repository.create_tables()
    location_service.load_locations_from_csv("uszips.csv")
    yield
    repository.drop_tables()

@pytest.fixture(autouse=True, scope="function")
def clean_db():
    car_repository.clear_table()
    cargo_repository.clear_table()
    pass
