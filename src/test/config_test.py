import os
from dotenv import load_dotenv

load_dotenv()

TEST_DB_HOST = os.environ["TEST_DB_HOST"]
TEST_DB_PORT = os.environ["TEST_DB_PORT"]
TEST_DB_NAME = os.environ["TEST_DB_NAME"]
TEST_DB_USER = os.environ["TEST_DB_USER"]
TEST_DB_PASS = os.environ["TEST_DB_PASS"]

SQLALCHEMY_DATABASE_URL_TEST = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"