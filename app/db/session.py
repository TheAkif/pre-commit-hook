from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if settings.TESTING:
    engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)