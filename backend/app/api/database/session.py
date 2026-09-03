from collections.abc import Generator

from app.api.database.connection import SessionLocal


def get_db() -> Generator:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
