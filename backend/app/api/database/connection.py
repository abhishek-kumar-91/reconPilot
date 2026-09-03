from sqlalchemy import JSON, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.api.core.config import settings


class Base(DeclarativeBase):
	pass


class Record(Base):
	__tablename__ = "recon_records"

	id: Mapped[str] = mapped_column(String(160), primary_key=True)
	kind: Mapped[str] = mapped_column(String(64), index=True)
	project_id: Mapped[str | None] = mapped_column(String(160), index=True)
	payload: Mapped[dict] = mapped_column(JSON)


class ProjectRecord(Base):
	__tablename__ = "projects"

	id: Mapped[str] = mapped_column(String(160), primary_key=True)
	name: Mapped[str] = mapped_column(String(255))
	root_domain: Mapped[str] = mapped_column(String(255), index=True)
	description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
	status: Mapped[str] = mapped_column(String(64))
	asset_count: Mapped[int] = mapped_column(default=0)
	endpoint_count: Mapped[int] = mapped_column(default=0)
	last_scan_at: Mapped[str | None] = mapped_column(String(64), nullable=True)
	created_at: Mapped[str] = mapped_column(String(64))


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def initialize_database() -> None:
	Base.metadata.create_all(bind=engine)
