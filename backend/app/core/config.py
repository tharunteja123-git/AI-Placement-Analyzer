from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url:str
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    embedding_model: str = "gemini-embedding-001"
    embedding_dim: int =768
    environment:str ="development"
    cors_origins:str =""
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")

    @property
    def cors_origin_list(self)->list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

settings=Settings()
