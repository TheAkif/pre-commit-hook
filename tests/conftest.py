from typing import Generator

import pytest, os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ['TESTING'] = 'true'

from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session", autouse=False)
def db() -> Generator:
    db = SessionLocal()
    init_db(db)
    yield db
    db.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as client:
        yield client
