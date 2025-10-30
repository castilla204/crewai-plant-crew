from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    dry_run: bool = True
    host: str = "0.0.0.0"
    port: int = 8010
    corpus_dir: str = "data/sops"

    @property
    def use_crewai(self) -> bool:
        return bool(self.openai_api_key) and not self.dry_run


settings = Settings()
