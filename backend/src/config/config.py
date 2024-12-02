from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Palytics App"
    app_description: str = "Patent infringement checker application"
    app_version: str = "0.0.1"
    PORT: int = 8000
    LLM_API_KEY: str
    FUZZY_MATCH_THRESHOLD: int = 80

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }

    @property
    def port(self) -> int:
        return self.PORT

    @property
    def llm_api_key(self) -> str:
        return self.LLM_API_KEY

    @property
    def fuzzy_match_threshold(self) -> int:
        return self.FUZZY_MATCH_THRESHOLD


@lru_cache()
def get_settings() -> Settings:
    return Settings(_env_file=".env")
