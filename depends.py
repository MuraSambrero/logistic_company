from repositories.location import LocationRepository
from repositories.cargo import CargoRepository
from repositories.car import CarRepository
from services.location import LocationService
from services.cargo import CargoService
from services.car import CarService
from db.db import DatabaseSessionManager
from config import SQLALCHEMY_DATABASE_URL

session_manager = DatabaseSessionManager(dsn_string=SQLALCHEMY_DATABASE_URL)

location_repository = LocationRepository(session_manager=session_manager)
cargo_repository = CargoRepository(session_manager=session_manager)
car_repository = CarRepository(session_manager=session_manager)

location_service = LocationService(location_repository)
car_service = CarService(car_repository)
cargo_service = CargoService(
    cargo_repository,
    location_service,
    car_service,
)


def get_location_service():
    return location_service


def get_cargo_service():
    return cargo_service


def get_car_service():
    return car_service
