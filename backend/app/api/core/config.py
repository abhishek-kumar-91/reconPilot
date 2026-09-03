from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	db_host: str = "localhost"
	db_port: int = 5432
	db_user: str = "postgres"
	db_password: str = ""
	db_name: str = "reconpilot"

	model_config = SettingsConfigDict(env_file=".env", extra="ignore")

	@property
	def database_url(self) -> str:
		return (
			f"postgresql+psycopg://{self.db_user}:{self.db_password}"
			f"@{self.db_host}:{self.db_port}/{self.db_name}"
		)


@lru_cache
def get_settings() -> Settings:
	return Settings()


settings = get_settings()
